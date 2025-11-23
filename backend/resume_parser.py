import io
from pypdf import PdfReader
from docx import Document

def parse_resume(file_content: bytes, filename: str) -> str:
    """
    Extracts text from PDF or DOCX resume.
    """
    text = ""
    try:
        if filename.lower().endswith('.pdf'):
            reader = PdfReader(io.BytesIO(file_content))
            for page in reader.pages:
                text += page.extract_text() + "\n"
        elif filename.lower().endswith('.docx'):
            doc = Document(io.BytesIO(file_content))
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            return "Unsupported file format. Please upload PDF or DOCX."
            
        return text.strip()
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return ""
