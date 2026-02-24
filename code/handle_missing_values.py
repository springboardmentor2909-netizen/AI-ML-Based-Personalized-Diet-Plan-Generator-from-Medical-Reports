import pandas as pd
from sklearn.impute import SimpleImputer

INPUT = r"C:\Users\Suman\Project\datasets\master_dataset_cleaned.csv"
OUTPUT = r"C:\Users\Suman\Project\datasets\master_dataset_imputed.csv"

df = pd.read_csv(INPUT)

numeric_cols = [
    "age", "height_cm", "weight_kg", "pulse",
    "bmi", "glucose", "cholesterol_total",
    "ldl", "hdl", "triglycerides",
    "hemoglobin", "creatinine"
]

imputer = SimpleImputer(strategy="median")
df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

df.to_csv(OUTPUT, index=False)
print("Missing values handled using MEDIAN →", OUTPUT)
