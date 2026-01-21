# nlp/ner_model.py
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

class MedicalNER:
    def __init__(self, model_name="dslim/bert-base-NER"):
        # Load a BERT NER model for medical entity extraction
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.nlp_pipeline = pipeline(
            "ner",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="simple"  # Merge tokens into meaningful entities
        )

    def extract_entities(self, text: str):
        """
        Extract entities from text.
        Returns a dictionary like:
        {
            "disease": ["diabetes", "hypertension"],
            "medication": ["metformin"],
            "lab_test": ["fbs", "cholesterol"]
        }
        """
        entities = {}
        ner_results = self.nlp_pipeline(text)
        for item in ner_results:
            label = item['entity_group'].lower()
            if label not in entities:
                entities[label] = []
            entities[label].append(item['word'])
        return entities
