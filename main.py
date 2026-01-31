import pandas as pd
import os
import argparse
from src.sanitizer import clean_data
from src.deduplicator import remove_duplicates
from src.categorizer import apply_categories
from src.reporter import summarize_by_month
from src.processor import load_data
from src.exporter import export_to_excel

def run_pipeline(file_path):
    """
    Orchestrates the full data pipeline from raw CSV to summary report.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find the file: {file_path}")

    # 1. Ingest
    print(f"--- Processing: {file_path} ---")
    raw_df = load_data(file_path)

    # 2. Sanitize (Dates and Amounts)
    clean_df = clean_data(raw_df)

    # 3. Deduplicate (Hashing logic)
    unique_df = remove_duplicates(clean_df)

    # 4. Categorize (JSON-based keyword matching)
    categorized_df = apply_categories(unique_df)

    # 5. Summarize (Monthly Pivot Table)
    report = summarize_by_month(categorized_df)

    return report

def main():
    # Setup CLI Argument Parsing
    parser = argparse.ArgumentParser(description="Personal Finance Pipeline")
    parser.add_argument("file", help="Path to the raw transaction CSV file")
    
    args = parser.parse_args()

    try:
        raw_df = load_data(args.file)
        cleaned_df = clean_data(raw_df)
        categorized_df = apply_categories(cleaned_df)
        summary_df = summarize_by_month(categorized_df)
        export_to_excel(summary_df, categorized_df)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()