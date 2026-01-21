from .preprocess_numeric import preprocess_numeric
from .preprocess_text import preprocess_text

if __name__ == "__main__":
    numeric_df = preprocess_numeric()
    text_df = preprocess_text()

    print("✅ Data preprocessing completed successfully")
