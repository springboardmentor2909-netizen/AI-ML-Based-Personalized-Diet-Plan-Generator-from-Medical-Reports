from PIL import Image, ImageFilter, ImageOps
import pytesseract

def extract_text_from_image(image_path: str) -> str:
    try:
        img = Image.open(image_path)
        # Convert to grayscale, enhance contrast
        img = img.convert('L')
        img = ImageOps.invert(img)  # invert if text is light on dark
        img = img.filter(ImageFilter.MedianFilter())
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"OCR extraction error: {e}")
        return ""
