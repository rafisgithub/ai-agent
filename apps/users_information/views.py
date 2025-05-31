from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UploadCvSerializer
from rest_framework.permissions import IsAuthenticated
from .models import UserInformation
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from .helper import download_hugging_face_embeddings,extract_text_from_cv, clean_text_for_latin1
from .prompt import university_recommendation_prompt,enrollment_assistance_prompt,migration_assistance_prompt,visa_processing_prompt
import mimetypes
import os
import tempfile
import json
import uuid
from PyPDF2 import PdfReader
import docx2txt
import unicodedata
import re
from werkzeug.utils import secure_filename


# load_dotenv()
# Load API Keys
# PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
# OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')



# Set up embeddings and vector store
embeddings = download_hugging_face_embeddings()
index_name = "tsernchimedkhi"
docsearch = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})


# Set up LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# CV extraction prompt
cv_extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert education counselor. Given a student's CV, extract their educational background, work experience, technical and soft skills, and study preferences."),
    ("human", "{cv_text}")
])
cv_extract_chain = LLMChain(prompt=cv_extraction_prompt, llm=llm)


 # Create a RAG chain from a prompt string
def build_rag_chain(prompt_text):
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_text),
        ("human", "{input}")
    ])
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, question_answer_chain)

# Prompt dictionary
PROMPT_SECTIONS = {
    "University Recommendations": university_recommendation_prompt,
    "Enrollment Assistance": enrollment_assistance_prompt,
    "Migration Advice": migration_assistance_prompt,
    "Visa Processing Guidance": visa_processing_prompt,
}
class UploadCvView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cv_file = request.FILES.get('cv_file', None)
        message = request.data.get('message', '')

        # Generate response based on user message
        rag_chain = build_rag_chain(university_recommendation_prompt)
        userMessageResponse = rag_chain.invoke({"input": message})

        structured_info = None
        pdf_sections = []

        if cv_file:
            file_name = secure_filename(cv_file.name)

            # Save uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1]) as tmp:
                for chunk in cv_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            # Extract raw text and structured info from CV
            raw_text = extract_text_from_cv(tmp_path)
            response = cv_extract_chain.invoke({"cv_text": raw_text})
            structured_info = response["text"]

            # Save for debugging or future analysis
            json_path = f"StudentData/cv_data_{uuid.uuid4().hex}.json"
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump({"cv_text": raw_text, "structured_info": structured_info}, f)

            # Run all RAG prompts using the extracted CV data
            for title, prompt in PROMPT_SECTIONS.items():
                rag_chain = build_rag_chain(prompt)
                result = rag_chain.invoke({"input": structured_info})
                pdf_sections.append((title, result["answer"]))

        # Save or update user information
        try:
            user_info = UserInformation.objects.get(custom_user=user)
            serializer = UploadCvSerializer(user_info, data=request.data, partial=True)
        except UserInformation.DoesNotExist:
            serializer = UploadCvSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(custom_user=request.user)

        # Prepare dynamic response
        response_data = {
            "response": userMessageResponse
        }

        if structured_info:
            response_data["cv_extracted_info"] = structured_info
            response_data["recommendations"] = {
                title: answer for title, answer in pdf_sections
            }

        return Response(response_data, status=status.HTTP_200_OK)
