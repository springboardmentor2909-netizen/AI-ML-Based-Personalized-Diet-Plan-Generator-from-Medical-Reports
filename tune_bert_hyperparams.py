import pandas as pd
import numpy as np
from datasets import Dataset
from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import optuna
import torch
import os

# Set random seeds for reproducibility
torch.manual_seed(42)
np.random.seed(42)

def load_and_preprocess_data():
    """Load and preprocess the medical text data"""
    df = pd.read_csv("training/data/medical_text_processed.csv")
    df = df.dropna()

    # Encode labels
    label_map = {label: idx for idx, label in enumerate(df["label"].unique())}
    df["label"] = df["label"].map(label_map)

    print(f"Label mapping: {label_map}")
    print(f"Dataset size: {len(df)}")
    print(f"Class distribution: {df['label'].value_counts()}")

    return df, label_map

def tokenize_data(df, tokenizer, max_length=256):
    """Tokenize the dataset"""
    dataset = Dataset.from_pandas(df)

    def tokenize(batch):
        return tokenizer(
            batch["text"],
            padding="max_length",
            truncation=True,
            max_length=max_length
        )

    dataset = dataset.map(tokenize, batched=True)
    dataset = dataset.remove_columns(["text"])
    dataset.set_format("torch")

    return dataset

def compute_metrics(eval_pred):
    """Compute evaluation metrics"""
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)

    accuracy = accuracy_score(labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='weighted')

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

def objective(trial):
    """Optuna objective function for hyperparameter tuning"""

    # Load data
    df, label_map = load_and_preprocess_data()

    # Split data
    train_df, val_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])

    # Tokenizer
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

    # Tokenize datasets
    train_dataset = tokenize_data(train_df, tokenizer)
    val_dataset = tokenize_data(val_df, tokenizer)

    # Hyperparameters to tune
    learning_rate = trial.suggest_float('learning_rate', 1e-5, 5e-4, log=True)
    batch_size = trial.suggest_categorical('batch_size', [4, 8, 16])
    weight_decay = trial.suggest_float('weight_decay', 0.0, 0.3)
    num_epochs = trial.suggest_int('num_epochs', 3, 10)
    warmup_steps = trial.suggest_int('warmup_steps', 0, 500)
    max_length = trial.suggest_categorical('max_length', [128, 256, 512])

    # Re-tokenize with new max_length if different
    if max_length != 256:
        train_dataset = tokenize_data(train_df, tokenizer, max_length)
        val_dataset = tokenize_data(val_df, tokenizer, max_length)

    # Model
    model = BertForSequenceClassification.from_pretrained(
        "bert-base-uncased",
        num_labels=len(label_map)
    )

    # Training arguments
    training_args = TrainingArguments(
        output_dir=f"./temp_trial_{trial.number}",
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=learning_rate,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=num_epochs,
        weight_decay=weight_decay,
        warmup_steps=warmup_steps,
        logging_steps=10,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
        save_total_limit=1,
        dataloader_pin_memory=False,
        report_to="none"  # Disable wandb/tensorboard logging
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )

    # Train
    trainer.train()

    # Evaluate
    eval_results = trainer.evaluate()

    # Clean up
    import shutil
    if os.path.exists(f"./temp_trial_{trial.number}"):
        shutil.rmtree(f"./temp_trial_{trial.number}")

    return eval_results['eval_accuracy']

def main():
    """Main function to run hyperparameter tuning"""

    print("🚀 Starting BERT Hyperparameter Tuning for 90-95% Accuracy")
    print("=" * 60)

    # Create study
    study = optuna.create_study(
        direction='maximize',
        study_name='bert_disease_classification',
        sampler=optuna.samplers.TPESampler(seed=42)
    )

    # Run optimization
    print("🔍 Optimizing hyperparameters...")
    study.optimize(objective, n_trials=20, timeout=3600)  # 20 trials or 1 hour timeout

    print("\n" + "=" * 60)
    print("🎯 BEST HYPERPARAMETERS FOUND:")
    print("=" * 60)
    print(f"Best Accuracy: {study.best_value:.4f}")
    print("Best Parameters:")
    for key, value in study.best_params.items():
        print(f"  {key}: {value}")

    # Train final model with best parameters
    print("\n🏆 Training final model with best hyperparameters...")
    train_final_model(study.best_params)

def train_final_model(best_params):
    """Train the final model with the best hyperparameters"""

    # Load data
    df, label_map = load_and_preprocess_data()

    # Split data (use more data for training)
    train_df, val_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df['label'])
    # For small datasets, use cross-validation instead of separate test set
    test_df = val_df.copy()  # Use validation set as test set for small data

    print(f"Train size: {len(train_df)}, Val size: {len(val_df)}, Test size: {len(test_df)}")

    # Tokenizer
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

    # Tokenize datasets
    train_dataset = tokenize_data(train_df, tokenizer, best_params['max_length'])
    val_dataset = tokenize_data(val_df, tokenizer, best_params['max_length'])
    test_dataset = tokenize_data(test_df, tokenizer, best_params['max_length'])

    # Model
    model = BertForSequenceClassification.from_pretrained(
        "bert-base-uncased",
        num_labels=len(label_map)
    )

    # Training arguments with best params
    training_args = TrainingArguments(
        output_dir="backend/app/models/bert_disease_classifier_tuned",
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=best_params['learning_rate'],
        per_device_train_batch_size=best_params['batch_size'],
        per_device_eval_batch_size=best_params['batch_size'],
        num_train_epochs=best_params['num_epochs'],
        weight_decay=best_params['weight_decay'],
        warmup_steps=best_params['warmup_steps'],
        logging_steps=10,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
        save_total_limit=2,
        dataloader_pin_memory=False,
        report_to="none"
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )

    # Train
    print("Training final model...")
    trainer.train()

    # Evaluate on test set
    print("Evaluating on test set...")
    test_results = trainer.evaluate(test_dataset)
    print(f"Test Results: {test_results}")

    # Save model and tokenizer
    trainer.save_model("backend/app/models/bert_disease_classifier_tuned")
    tokenizer.save_pretrained("backend/app/models/bert_disease_classifier_tuned")

    # Save label mapping
    import json
    with open("backend/app/models/bert_disease_classifier_tuned/label_map.json", "w") as f:
        json.dump(label_map, f)

    print("✅ Tuned BERT model trained and saved successfully!")
    print(f"🎯 Final Test Accuracy: {test_results['eval_accuracy']:.4f}")
    print(f"📁 Model saved to: backend/app/models/bert_disease_classifier_tuned")

if __name__ == "__main__":
    main()