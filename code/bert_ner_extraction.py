import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import ast
import pandas as pd
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# FILE PATHS
INPUT_FILE = r"C:\Users\Suman\Project\datasets\doctor_notes_cleaned_segmented.csv"
OUTPUT_FILE = r"C:\Users\Suman\Project\datasets\doctor_notes_with_entities.csv"

TEXT_COLUMN = "cleaned_doctor_sentences"

# LOAD BERT NER MODEL (Biomedical)
MODEL_NAME = "d4data/biomedical-ner-all"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)

ner_pipeline = pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"   # merges word pieces
)

# EXTRACT ENTITIES FROM SENTENCES
def extract_entities(sentences):
    entities = []

    if not isinstance(sentences, list):
        return entities

    for sentence in sentences:
        try:
            ner_results = ner_pipeline(sentence)
            for ent in ner_results:
                entities.append({
                    "text": ent["word"],
                    "label": ent["entity_group"],
                    "score": round(ent["score"], 3)
                })
        except Exception:
            continue

    return entities

# PROCESS DATASET
def process_dataset():
    df = pd.read_csv(INPUT_FILE)

    # Convert string list → Python list
    df[TEXT_COLUMN] = df[TEXT_COLUMN].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else []
    )

    print("Running BERT NER on doctor notes...")

    df["medical_entities"] = df[TEXT_COLUMN].apply(extract_entities)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nBERT NER extraction completed successfully")
    print(f"Saved to: {OUTPUT_FILE}")

# RUN
if __name__ == "__main__":
    process_dataset()
