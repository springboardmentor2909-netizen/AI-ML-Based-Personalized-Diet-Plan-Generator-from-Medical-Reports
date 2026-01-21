# reports/json_exporter.py
import json
from pathlib import Path

JSON_DIR = Path("reports/generated_jsons")

def export_json(patient_id: str, diet_json: dict) -> str:
    """
    Saves the actionable diet plan as a JSON file for download.
    
    Returns the path to the saved JSON.
    """
    try:
        # Ensure output folder exists
        JSON_DIR.mkdir(parents=True, exist_ok=True)
        json_path = JSON_DIR / f"{patient_id}_diet_plan.json"

        with open(json_path, "w") as f:
            json.dump(diet_json, f, indent=4)

        return str(json_path)

    except Exception as e:
        print(f"❌ Error exporting JSON: {e}")
        return ""
