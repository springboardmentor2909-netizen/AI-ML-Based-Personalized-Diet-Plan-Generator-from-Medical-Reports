import pandas as pd

# PATHS
INPUT = r"C:\Users\Suman\Project\datasets\master_dataset_imputed.csv"
OUTPUT = r"C:\Users\Suman\Project\datasets\master_dataset_normalized.csv"

df = pd.read_csv(INPUT)

# Numeric columns EXCLUDING BP
numeric_cols = [
    "age",
    "height_cm",
    "weight_kg",
    "pulse",
    "bmi",
    "glucose",
    "cholesterol_total",
    "ldl",
    "hdl",
    "triglycerides",
    "hemoglobin",
    "creatinine"
]

# Min–Max Normalization
for col in numeric_cols:
    min_val = df[col].min()
    max_val = df[col].max()
    if min_val != max_val:
        df[col + "_norm"] = (df[col] - min_val) / (max_val - min_val)
    else:
        df[col + "_norm"] = 0.0

df.to_csv(OUTPUT, index=False)
print("Normalization (without BP) complete →", OUTPUT)
