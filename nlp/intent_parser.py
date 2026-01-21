# # nlp/intent_parser.py
# from nlp.ner_model import MedicalNER

# class IntentParser:
#     def __init__(self, device: int = -1):
#         """
#         Initialize NER model for parsing medical intent.
#         """
#         self.ner = MedicalNER(device=device)

#     def parse_intent(self, text: str):
#         """
#         Converts clinical notes into structured medical intent.
#         Returns a string summarizing key conditions.
#         """
#         entities = self.ner.extract_entities(text)
#         if not entities:
#             return text  # If no entities, return original text
#         return ", ".join(entities)



from nlp.ner_model import MedicalNER

class IntentParser:
    def __init__(self):
        self.ner = MedicalNER()

    def parse_intent(self, text, entities):
        return {
            "summary": text[:300],
            "entities": entities
        }
