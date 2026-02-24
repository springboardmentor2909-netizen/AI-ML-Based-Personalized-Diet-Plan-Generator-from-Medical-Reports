import pandas as pd
import ast

# FILE PATHS
INPUT_FILE = r"C:\Users\Suman\Project\datasets\doctor_notes_with_entities.csv"
OUTPUT_FILE = r"C:\Users\Suman\Project\datasets\doctor_notes_with_medical_intents.csv"

ENTITY_COLUMN = "medical_entities"
SENTENCE_COLUMN = "cleaned_doctor_sentences"

# RULE DICTIONARY (EXPLAINABLE MEDICAL LOGIC)
MEDICAL_RULES = {
    "LOW_SODIUM_DIET": [
        "blood pressure", "hypertension", "bp", "salt", "sodium"
    ],
    "LOW_SUGAR_DIET": [
        "diabetes", "glucose", "blood sugar", "hba1c"
    ],
    "LOW_FAT_DIET": [
        "cholesterol", "ldl", "triglycerides", "lipid"
    ],
    "WEIGHT_MANAGEMENT_DIET": [
        "obesity", "overweight", "bmi", "weight gain"
    ],
    "IRON_RICH_DIET": [
        "anemia", "hemoglobin", "hb", "iron"
    ],
    "LIFESTYLE_MODIFICATION": [
        "exercise", "physical activity", "lifestyle", "diet"
    ]
}

# INTENT EXTRACTION FUNCTION
def extract_medical_intents(entities, sentences):
    intents = set()
    evidence = []

    combined_text = " ".join(sentences).lower()

    for intent, keywords in MEDICAL_RULES.items():
        for kw in keywords:
            if kw in combined_text:
                intents.add(intent)
                evidence.append(f"Matched '{kw}' for {intent}")
                break

    if not intents:
        intents.add("GENERAL_HEALTHY_DIET")
        evidence.append("No specific condition detected")

    return list(intents), evidence

# PROCESS DATASET
def process_dataset():
    df = pd.read_csv(INPUT_FILE)

    if ENTITY_COLUMN not in df.columns:
        raise ValueError(f"Missing column: {ENTITY_COLUMN}")

    if SENTENCE_COLUMN not in df.columns:
        raise ValueError(f"Missing column: {SENTENCE_COLUMN}")

    medical_intents = []
    intent_evidence = []

    for _, row in df.iterrows():
        entities = row[ENTITY_COLUMN]
        sentences = row[SENTENCE_COLUMN]

        # Parse stringified lists safely
        if isinstance(entities, str):
            try:
                entities = ast.literal_eval(entities)
            except:
                entities = []

        if isinstance(sentences, str):
            try:
                sentences = ast.literal_eval(sentences)
            except:
                sentences = []

        intents, evidence = extract_medical_intents(entities, sentences)

        medical_intents.append(intents)
        intent_evidence.append(evidence)

    df["medical_intents"] = medical_intents
    df["intent_evidence"] = intent_evidence

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nRule-based medical intent extraction completed successfully")
    print(f"Saved to: {OUTPUT_FILE}")

    print("\nSample output:")
    print(df[[SENTENCE_COLUMN, "medical_intents"]].head())

# RUN
if __name__ == "__main__":
    process_dataset()
