import re

class TextCleaner:
    def __init__(self):
        pass

    def clean_text(self, text: str) -> str:
        """
        Cleans raw text from PDFs, images, or doctor notes.
        Steps:
        - Lowercase
        - Remove extra whitespaces
        - Remove special characters (except . ,)
        """
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,]', '', text)
        return text.strip()

    def segment_text(self, text: str, max_len: int = 512):
        """
        Optional: Splits long notes into segments for model processing
        """
        words = text.split()
        for i in range(0, len(words), max_len):
            yield " ".join(words[i:i + max_len])
