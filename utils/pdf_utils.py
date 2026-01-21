
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from PDF.
    Handles both digital PDFs and scanned PDFs (using OCR).
    """
    try:
        doc = fitz.open(pdf_file)
        full_text = ""
        for page in doc:
            text = page.get_text()
            if not text.strip():  # scanned PDF
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes()))
                text = pytesseract.image_to_string(img)
            full_text += text + "\n"
        doc.close()
        return full_text.strip()
    except Exception as e:
        print(f"❌ PDF extraction error: {e}")
        return ""
