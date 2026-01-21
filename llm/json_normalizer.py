# llm/json_normalizer.py
import json

class JSONNormalizer:
    """
    Ensures LLM outputs are strictly formatted JSON for downstream processing.
    """

    @staticmethod
    def normalize(diet_dict: dict) -> dict:
        """
        Input: diet_dict from LLM (might have formatting issues)
        Output: strict JSON with keys 'recommendation' and 'avoid'
        """
        try:
            # If already string, try parsing
            if isinstance(diet_dict, str):
                diet_dict = json.loads(diet_dict.replace("'", '"'))

            # Ensure required keys exist
            recommendations = diet_dict.get("recommendation", [])
            avoid = diet_dict.get("avoid", "")

            # Ensure recommendation is always a list
            if not isinstance(recommendations, list):
                recommendations = [recommendations]

            # Ensure avoid is always a string
            if not isinstance(avoid, str):
                avoid = str(avoid)

            return {
                "recommendation": recommendations,
                "avoid": avoid
            }

        except Exception as e:
            print(f"❌ JSON normalization error: {e}")
            # Fallback
            return {
                "recommendation": [],
                "avoid": ""
            }
