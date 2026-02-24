import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb
from xgboost import XGBClassifier

# LOAD DATA
DATASET = r"C:\Users\Suman\Project\datasets\master_dataset_ready_for_ml.csv"
df = pd.read_csv(DATASET)

# Binary target: Normal (0) / Abnormal (1)
df["final_health_label"] = (
    (df["diabetic_risk"] == 1) |
    (df["hypertension_risk"] == 1) |
    (df["obesity_risk"] == 1) |
    (df["anemia_risk"] == 1)
).astype(int)

FEATURES = [
    "age_norm", "height_cm_norm", "weight_kg_norm",
    "pulse_norm", "glucose_norm",
    "cholesterol_total_norm", "ldl_norm", "hdl_norm",
    "triglycerides_norm", "hemoglobin_norm",
    "creatinine_norm", "bp_systolic_norm",
    "bp_diastolic_norm", "gender_encoded"
]

X = df[FEATURES]
y = df["final_health_label"]

# SPLIT DATA
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# MODELS
MODELS = {
    "RandomForest": RandomForestClassifier(
        n_estimators=350,
        max_depth=15,
        min_samples_leaf=5,
        min_samples_split=10,
        random_state=42,
        n_jobs=-1
    ),

    "LightGBM": lgb.LGBMClassifier(
        objective="binary",
        learning_rate=0.05,
        n_estimators=250,              # fewer trees
        max_depth=3,                   # very shallow trees
        num_leaves=8,                  # force overlap
        min_child_samples=120,         # STRONG
        min_split_gain=0.2,            # block small gains
        subsample=0.6,
        colsample_bytree=0.6,
        reg_alpha=1.0,
        reg_lambda=2.0,
        random_state=42,
        verbosity=-1
    ),


    "XGBoost": XGBClassifier(
        objective="binary:logistic",
        n_estimators=350,
        learning_rate=0.05,
        max_depth=5,
        min_child_weight=10,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.3,
        reg_lambda=1.0,
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1
    )
}

# TRAIN vs TEST EVALUATION
print("\n" + "=" * 90)
print("TRAIN vs TEST PERFORMANCE (NORMAL vs ABNORMAL)")
print("=" * 90)

THRESHOLD = 0.45 

for name, model in MODELS.items():
    print(f"\n{name}")
    print("-" * 60)

    model.fit(X_train, y_train)

    # TRAIN
    train_prob = model.predict_proba(X_train)[:, 1]
    train_pred = (train_prob >= THRESHOLD).astype(int)

    # TEST
    test_prob = model.predict_proba(X_test)[:, 1]
    test_pred = (test_prob >= THRESHOLD).astype(int)

    print(
        f"TRAIN -> "
        f"Acc: {accuracy_score(y_train, train_pred):.4f} | "
        f"Prec: {precision_score(y_train, train_pred):.4f} | "
        f"Recall: {recall_score(y_train, train_pred):.4f} | "
        f"F1: {f1_score(y_train, train_pred):.4f} | "
        f"AUC: {roc_auc_score(y_train, train_prob):.4f}"
    )

    print(
        f"TEST  -> "
        f"Acc: {accuracy_score(y_test, test_pred):.4f} | "
        f"Prec: {precision_score(y_test, test_pred):.4f} | "
        f"Recall: {recall_score(y_test, test_pred):.4f} | "
        f"F1: {f1_score(y_test, test_pred):.4f} | "
        f"AUC: {roc_auc_score(y_test, test_prob):.4f}"
    )
