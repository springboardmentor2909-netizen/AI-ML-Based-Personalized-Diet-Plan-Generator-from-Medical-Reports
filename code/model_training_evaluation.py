import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix
)

from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb
from xgboost import XGBClassifier

DATASET = r"C:\Users\Suman\Project\datasets\master_dataset_ready_for_ml.csv"
df = pd.read_csv(DATASET)

# FINAL BINARY TARGET (Normal vs Abnormal)
df["final_health_label"] = np.where(
    (df["diabetic_risk"] == 1) |
    (df["hypertension_risk"] == 1) |
    (df["obesity_risk"] == 1) |
    (df["anemia_risk"] == 1),
    1,  # Abnormal
    0   # Normal
)

# FEATURES
FEATURES = [
    "age_norm", "height_cm_norm", "weight_kg_norm", "bmi_norm",
    "pulse_norm", "glucose_norm",
    "cholesterol_total_norm", "ldl_norm", "hdl_norm",
    "triglycerides_norm", "hemoglobin_norm", "creatinine_norm",
    "bp_systolic_norm", "bp_diastolic_norm",
    "gender_encoded"
]

X = df[FEATURES]
y = df["final_health_label"]

# TRAIN–TEST SPLIT 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.20, random_state=42
)

# Handle imbalance
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

# MODELS
models = {
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

# CROSS-VALIDATION EVALUATION
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

def evaluate_model_cv(model, X, y):
    metrics = {
        "accuracy": [],
        "precision": [],
        "recall": [],
        "f1": [],
        "roc_auc": []
    }

    for train_idx, val_idx in cv.split(X, y):
        X_tr, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_tr, y_val = y.iloc[train_idx], y.iloc[val_idx]

        model.fit(X_tr, y_tr)

        y_pred = model.predict(X_val)
        y_prob = model.predict_proba(X_val)[:, 1]

        metrics["accuracy"].append(accuracy_score(y_val, y_pred))
        metrics["precision"].append(precision_score(y_val, y_pred))
        metrics["recall"].append(recall_score(y_val, y_pred))
        metrics["f1"].append(f1_score(y_val, y_pred))
        metrics["roc_auc"].append(roc_auc_score(y_val, y_prob))

    return {
        m: (np.mean(v), np.std(v))
        for m, v in metrics.items()
    }

# RUN TRAINING + CV EVALUATION
print("\n" + "="*90)
print("FINAL MODEL EVALUATION (NORMAL vs ABNORMAL)")
print("="*90)

for name, model in models.items():
    print(f"\n{name}")
    print("-"*60)

    results = evaluate_model_cv(model, X_train, y_train)

    for metric, (mean, std) in results.items():
        print(f"{metric.upper():10s}: {mean:.4f} ± {std:.4f}")

    # Final test evaluation
    model.fit(X_train, y_train)
    test_preds = model.predict(X_test)

    print("\nTest Set Confusion Matrix:")
    print(confusion_matrix(y_test, test_preds))
