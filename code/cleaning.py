import pandas as pd
import numpy as np

INPUT = r"C:\Users\Suman\Project\datasets\master_dataset.csv"
OUTPUT = r"C:\Users\Suman\Project\datasets\master_dataset_cleaned.csv"

df = pd.read_csv(INPUT)
print("Initial shape:", df.shape)

# BASIC CLEANING
df.loc[(df["age"] < 1) | (df["age"] > 120), "age"] = np.nan

df["gender"] = df["gender"].str.strip().str.capitalize()

df["gender"] = df["gender"].replace({
    "M": "Male",
    "F": "Female",
    "Other": "Others",
    "Others": "Others"
})

df.loc[~df["gender"].isin(["Male", "Female", "Others"]), "gender"] = np.nan


df.loc[(df["height_cm"] < 50) | (df["height_cm"] > 250), "height_cm"] = np.nan
df.loc[(df["weight_kg"] < 10) | (df["weight_kg"] > 300), "weight_kg"] = np.nan

df.loc[(df["pulse"] < 30) | (df["pulse"] > 200), "pulse"] = np.nan
df.loc[(df["bmi"] < 10) | (df["bmi"] > 80), "bmi"] = np.nan

df.loc[(df["glucose"] < 50) | (df["glucose"] > 500), "glucose"] = np.nan
df.loc[(df["cholesterol_total"] < 50) | (df["cholesterol_total"] > 400), "cholesterol_total"] = np.nan

# LIPID PROFILE
df.loc[(df["ldl"] < 20) | (df["ldl"] > 300), "ldl"] = np.nan
df.loc[(df["hdl"] < 10) | (df["hdl"] > 120), "hdl"] = np.nan
df.loc[(df["triglycerides"] < 40) | (df["triglycerides"] > 600), "triglycerides"] = np.nan

df.loc[(df["hemoglobin"] < 5) | (df["hemoglobin"] > 20), "hemoglobin"] = np.nan
df.loc[(df["creatinine"] < 0.2) | (df["creatinine"] > 6), "creatinine"] = np.nan

df.to_csv(OUTPUT, index=False)
print("Data cleaned →", OUTPUT)
