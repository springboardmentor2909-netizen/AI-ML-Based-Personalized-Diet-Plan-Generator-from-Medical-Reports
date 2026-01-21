import pandas as pd
import os

def preprocess_text():
    print("Loading text data...")

    input_path = "training/data/medical_text.csv"
    output_path = "training/data/medical_text_processed.csv"

    df = pd.read_csv(input_path)

    print("Text rows before cleaning:", len(df))

    df.dropna(subset=["text", "label"], inplace=True)
    df["text"] = df["text"].astype(str).str.lower()

    os.makedirs("training/data", exist_ok=True)
    df.to_csv(output_path, index=False)

    print("Text rows after cleaning:", len(df))
    print("Saved to:", output_path)

    return df
