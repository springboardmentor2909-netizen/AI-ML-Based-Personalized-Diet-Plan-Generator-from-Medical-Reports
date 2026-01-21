# utils/file_utils.py
import os
import shutil
from pathlib import Path

TEMP_DIR = Path("data/temp")

def save_uploaded_file(uploaded_file) -> str:
    """
    Saves an uploaded file to the temp directory and returns the file path.
    """
    try:
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        file_path = TEMP_DIR / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return str(file_path)
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return ""

def clear_temp_dir():
    """
    Clears all files from the temp directory.
    """
    try:
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)
            TEMP_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"❌ Error clearing temp directory: {e}")
