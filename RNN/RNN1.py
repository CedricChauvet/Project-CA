import fitz  # PyMuPDF
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def preprocess_text(text):
    sentences = sent_tokenize(text)
    return sentences