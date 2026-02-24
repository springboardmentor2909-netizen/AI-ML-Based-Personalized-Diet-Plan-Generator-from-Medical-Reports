import pandas as pd
import os

# Paths to your 3 CSVs
TEXT_CSV = r"C:\Users\Suman\Project\datasets\text_reports_structured_data.csv"
PDF_CSV = r"C:\Users\Suman\Project\datasets\pdf_reports_structured_data.csv"
IMAGE_CSV = r"C:\Users\Suman\Project\datasets\png_reports_structured_data.csv"

OUTPUT = r"C:\Users\Suman\Project\datasets\master_dataset.csv"

dfs = []

# Load TEXT CSV if exists
if os.path.exists(TEXT_CSV):
    print("Loading TEXT CSV...")
    dfs.append(pd.read_csv(TEXT_CSV))

# Load IMAGE CSV if exists
if os.path.exists(IMAGE_CSV):
    print("Loading IMAGE CSV...")
    dfs.append(pd.read_csv(IMAGE_CSV))

# Load PDF CSV if exists
if os.path.exists(PDF_CSV):
    print("Loading PDF CSV...")
    dfs.append(pd.read_csv(PDF_CSV))

# Merge all
if dfs:
    master_df = pd.concat(dfs, ignore_index=True)
    master_df.to_csv(OUTPUT, index=False)
    print("MERGE COMPLETE →", OUTPUT)
else:
    print("No CSV files found!")
