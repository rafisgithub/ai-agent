from langchain.embeddings import HuggingFaceEmbeddings
import uuid
from PyPDF2 import PdfReader
import docx2txt
import unicodedata
import re


def download_hugging_face_embeddings():
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')


# Extract text from CV files

def extract_text_from_cv(file_path):
    ext = file_path.split('.')[-1].lower()
    if ext == 'pdf':
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    elif ext in ['doc', 'docx']:
        return docx2txt.process(file_path)
    else:
        raise ValueError("Unsupported file format")
    
# Clean text to remove problematic Unicode characters
def clean_text_for_latin1(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("latin-1", errors="ignore").decode("latin-1")
    text = re.sub(r"[\*\_`]", "", text)
    return text

