from transformers import BertTokenizer, BertForSequenceClassification
import os

MODEL_DIR = "backend/app/models/bert_disease_classifier"

os.makedirs(MODEL_DIR, exist_ok=True)

# Load pretrained BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=4  # diabetes, heart_disease, healthy, thyroid
)

# Save model and tokenizer
model.save_pretrained(MODEL_DIR)
tokenizer.save_pretrained(MODEL_DIR)

print("✅ Pretrained BERT model saved successfully")
print(f"📁 Location: {MODEL_DIR}")
