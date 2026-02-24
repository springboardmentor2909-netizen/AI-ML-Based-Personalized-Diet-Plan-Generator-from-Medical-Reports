import pandas as pd
import re
import nltk
from nltk.tokenize import sent_tokenize

# DOWNLOAD REQUIRED NLTK DATA
nltk.download("punkt")
nltk.download("punkt_tab")

# FILE PATHS
INPUT_FILE = r"C:\Users\Suman\Project\datasets\master_dataset_ready_for_ml.csv"
OUTPUT_FILE = r"C:\Users\Suman\Project\datasets\doctor_notes_cleaned_segmented.csv"

TEXT_COLUMN = "doctor_comments"

# TEXT CLEANING + SEGMENTATION
def clean_and_segment(text):
    if pd.isna(text) or not isinstance(text, str):
        return []

    # lowercase
    text = text.lower()

    # remove special characters but keep medical symbols
    text = re.sub(r"[^a-zA-Z0-9.%/\s]", " ", text)

    # normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    # sentence segmentation
    sentences = sent_tokenize(text)

    # remove very short / noisy sentences
    sentences = [
        s.strip()
        for s in sentences
        if len(s.strip()) > 5
    ]

    return sentences

# PROCESS DATASET (KEEP EVERYTHING)
def process_dataset(input_path, output_path):
    df = pd.read_csv(input_path)

    if TEXT_COLUMN not in df.columns:
        raise ValueError(f"Column '{TEXT_COLUMN}' not found in dataset")

    # ADD new column, do NOT drop anything
    df["cleaned_doctor_sentences"] = df[TEXT_COLUMN].apply(clean_and_segment)

    # Save full dataset to NEW file
    df.to_csv(output_path, index=False)

    print("\nText cleaning & segmentation completed successfully")
    print("All original columns preserved")
    print(f"Saved to: {output_path}")

# RUN
if __name__ == "__main__":
    process_dataset(INPUT_FILE, OUTPUT_FILE)
