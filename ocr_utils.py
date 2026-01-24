import easyocr
from PIL import Image
import numpy as np

# Initialize reader once
reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image_file):
    image = Image.open(image_file).convert("RGB")
    image_np = np.array(image)

    results = reader.readtext(image_np, detail=0)
    text = " ".join(results)

    return text.strip()
