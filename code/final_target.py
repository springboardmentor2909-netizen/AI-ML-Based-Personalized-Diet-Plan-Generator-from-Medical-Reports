import pandas as pd
import numpy as np

df = pd.read_csv(
    r"C:\Users\Suman\Project\datasets\master_dataset_preprocessed.csv"
)


# Disease / Condition Risk Flags

# Diabetes
df["diabetic_risk"] = (df["glucose"] >= 126).astype(int)

# Hypertension
df["hypertension_risk"] = (
    (df["bp_systolic"] >= 140) |
    (df["bp_diastolic"] >= 90)
).astype(int)

# Obesity
df["obesity_risk"] = (df["bmi"] >= 30).astype(int)

# Anemia (gender-aware)
def anemia_flag(row):
    if pd.isna(row["hemoglobin"]) or pd.isna(row["gender_encoded"]):
        return 0
    if row["gender_encoded"] == 1:   # Male
        return int(row["hemoglobin"] < 13)
    else:                             # Female / Others
        return int(row["hemoglobin"] < 12)

df["anemia_risk"] = df.apply(anemia_flag, axis=1)

# FINAL HEALTH STATUS (NORMAL / ABNORMAL)
df["final_health_status"] = (
    (df["diabetic_risk"] == 1) |
    (df["hypertension_risk"] == 1) |
    (df["obesity_risk"] == 1) |
    (df["anemia_risk"] == 1)
).astype(int)

# Optional readable label
df["final_health_label"] = df["final_health_status"].map({
    0: "Normal",
    1: "Abnormal"
})

# Save final dataset
df.to_csv(
    r"C:\Users\Suman\Project\datasets\master_dataset_ready_for_ml.csv",
    index=False
)


print(df[[
    "diabetic_risk",
    "hypertension_risk",
    "obesity_risk",
    "anemia_risk",
    "final_health_label"
]].value_counts())
