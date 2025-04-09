import pdfplumber
import docx
import os


def extract_text_from_document(file):
    """
    Extracts text from a PDF or DOCX file-like object.
    
    Returns:
        The extracted text, or an error message if extraction fails or the file type is unsupported.
    """
    file_extension = os.path.splitext(file.name)[1].lower()
    text = ""
    
    if file_extension == ".pdf":
        try:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            text = f"Error extracting PDF text: {str(e)}"
    
    elif file_extension == ".docx":
        try:
            doc = docx.Document(file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            text = f"Error extracting DOCX text: {str(e)}"
    
    else:
        text = "Unsupported file format. Please upload a PDF or DOCX file."
    
    return text

