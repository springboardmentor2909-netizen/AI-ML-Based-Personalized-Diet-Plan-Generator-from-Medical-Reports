import pytesseract
from PIL import Image
import pdfplumber
import io
from pdf2image import convert_from_bytes

# ✅ Tesseract executable path (uncomment if needed)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(file_bytes: bytes, filename: str) -> str:
    try:
        if filename.lower().endswith(".pdf"):
            # Try pdfplumber first for text-based PDFs
            text = ""
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text.strip()
            
            # If no text extracted, treat as scanned PDF and use OCR
            images = convert_from_bytes(file_bytes)
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image) + "\n"
            return text.strip()
        else:
            image = Image.open(io.BytesIO(file_bytes))
            return pytesseract.image_to_string(image).strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""
