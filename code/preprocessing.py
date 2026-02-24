import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

# PATHS
INPUT = r"C:\Users\Suman\Project\datasets\master_dataset_normalized.csv"
OUTPUT = r"C:\Users\Suman\Project\datasets\master_dataset_preprocessed.csv"

df = pd.read_csv(INPUT)
print("Loaded shape:", df.shape)


# BLOOD PRESSURE SPLITTING
def split_bp(bp):
    if isinstance(bp, str) and "/" in bp:
        try:
            s, d = bp.split("/")
            return int(s.strip()), int(d.strip())
        except:
            return np.nan, np.nan
    return np.nan, np.nan

df[["bp_systolic", "bp_diastolic"]] = df["bp"].apply(
    lambda x: pd.Series(split_bp(x))
)

df.drop(columns=["bp"], inplace=True)

# BP RANGE CLEANING
df.loc[(df["bp_systolic"] < 70) | (df["bp_systolic"] > 200), "bp_systolic"] = np.nan
df.loc[(df["bp_diastolic"] < 40) | (df["bp_diastolic"] > 130), "bp_diastolic"] = np.nan

# BP IMPUTATION (MEDIAN)
bp_imputer = SimpleImputer(strategy="median")
df[["bp_systolic", "bp_diastolic"]] = bp_imputer.fit_transform(
    df[["bp_systolic", "bp_diastolic"]]
)

# BP NORMALIZATION
for col in ["bp_systolic", "bp_diastolic"]:
    min_val = df[col].min()
    max_val = df[col].max()
    if min_val != max_val:
        df[col + "_norm"] = (df[col] - min_val) / (max_val - min_val)
    else:
        df[col + "_norm"] = 0.0

# GENDER ENCODING 
gender_map = {
    "Male": 0,
    "Female": 1,
    "Others": 2
}
df["gender_encoded"] = df["gender"].map(gender_map)


# BMI CATEGORY
def bmi_category(bmi):
    if pd.isna(bmi):
        return np.nan
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

df["bmi_category"] = df["bmi"].apply(bmi_category)

# BP CATEGORY
def bp_category(sys, dia):
    if pd.isna(sys) or pd.isna(dia):
        return np.nan
    if sys < 120 and dia < 80:
        return "Normal"
    elif sys < 140 or dia < 90:
        return "Prehypertension"
    else:
        return "Hypertension"

df["bp_category"] = df.apply(
    lambda x: bp_category(x["bp_systolic"], x["bp_diastolic"]),
    axis=1
)

# HEALTH RISK FLAGS
df["diabetic_risk"] = (df["glucose"] >= 126).astype(int)
df["hypertension_risk"] = (
    (df["bp_systolic"] >= 140) | (df["bp_diastolic"] >= 90)
).astype(int)
df["obesity_risk"] = (df["bmi"] >= 30).astype(int)
df["anemia_risk"] = (df["hemoglobin"] < 12).astype(int)

# SAVE
df.to_csv(OUTPUT, index=False)
print("Preprocessing complete")
print("Final shape:", df.shape)
