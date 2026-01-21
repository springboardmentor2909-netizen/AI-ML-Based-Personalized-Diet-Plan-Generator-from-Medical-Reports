import pandas as pd
import os

def preprocess_numeric():
    print("Loading numeric data...")

    input_path = "training/data/medical_numeric.csv"
    output_path = "training/data/medical_numeric_processed.csv"

    df = pd.read_csv(input_path)
    df.fillna(df.mean(numeric_only=True), inplace=True)

    os.makedirs("training/data", exist_ok=True)
    df.to_csv(output_path, index=False)

    print("Numeric data shape:", df.shape)
    print("Saved to:", output_path)

    return df
