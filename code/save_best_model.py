import pandas as pd
import numpy as np
import joblib

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
# SAVE TRAINING FEATURE ORDER (VERY IMPORTANT FOR INFERENCE)
pd.DataFrame({"feature": X_train.columns}).to_csv(
    r"C:\Users\Suman\Project\models\train_columns.csv",
    index=False
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
        learning_rate=0.03,
        class_weight="balanced",
        n_estimators=400,
        max_depth=5,
        num_leaves=16,
        min_child_samples=40,
        subsample=0.75,
        colsample_bytree=0.75,
        reg_alpha=0.5,
        reg_lambda=0.7,
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

# EVALUATION + BEST MODEL SELECTION
results = []
trained_models = {}

print("\n" + "=" * 90)
print("MODEL COMPARISON USING ALL METRICS")
print("=" * 90)

for name, model in MODELS.items():
    model.fit(X_train, y_train)
    trained_models[name] = model

    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds)
    rec = recall_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    auc = roc_auc_score(y_test, probs)

    # Composite score (uses ALL metrics)
    composite = (
        0.20 * acc +
        0.20 * prec +
        0.20 * rec +
        0.25 * f1 +
        0.15 * auc
    )

    results.append([
        name, acc, prec, rec, f1, auc, composite
    ])

    print(f"\n{name}")
    print("-" * 50)
    print(f"Accuracy   : {acc:.4f}")
    print(f"Precision  : {prec:.4f}")
    print(f"Recall     : {rec:.4f}")
    print(f"F1-score   : {f1:.4f}")
    print(f"ROC-AUC    : {auc:.4f}")
    print(f"Composite  : {composite:.4f}")

# SELECT & SAVE BEST MODEL
results_df = pd.DataFrame(
    results,
    columns=[
        "Model", "Accuracy", "Precision", "Recall",
        "F1", "ROC_AUC", "CompositeScore"
    ]
)

best_row = results_df.sort_values(
    by="CompositeScore", ascending=False
).iloc[0]

best_model_name = best_row["Model"]
best_model = trained_models[best_model_name]

MODEL_PATH = r"C:\Users\Suman\Project\models\best_diet_planning_model.pkl"
joblib.dump(best_model, MODEL_PATH)

print("\n" + "=" * 90)
print("BEST MODEL SELECTED USING ALL METRICS")
print("=" * 90)
print(results_df)
print(f"\nBest Model : {best_model_name}")
print(f"Saved to   : {MODEL_PATH}")
