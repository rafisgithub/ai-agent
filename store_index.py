from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


load_dotenv()
PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


def load_pdf_file(data):
    loader= DirectoryLoader(data,
        glob="*.pdf",
        loader_cls=PyPDFLoader)

    documents=loader.load()
    return documents
#Split the Data into Text Chunks
def text_split(extracted_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks=text_splitter.split_documents(extracted_data)
    return text_chunks
def download_hugging_face_embeddings():
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

extracted_data=load_pdf_file(data='data/')
text_chunks=text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "tsernchimedkhi"


pc.create_index(
    name=index_name,
    dimension=384, 
    metric="cosine", 
    spec=ServerlessSpec(
        cloud="aws", 
        region="us-east-1"
    )
) 

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings, 
)