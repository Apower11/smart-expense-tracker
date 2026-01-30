import json
import os
import pandas as pd

def load_categories(config_path='config/categories.json'):
    """
    Reads the keyword mapping from the JSON config file.
    Returns an empty dict if the file is missing or malformed.
    """
    if not os.path.exists(config_path):
        # Using a simple print for now; consider logging module for production
        print(f"(!) Warning: {config_path} not found. Defaulting to 'Other'.")
        return {}
        
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"(!) Error: {config_path} is not valid JSON.")
        return {}

def apply_categories(df, config_path='config/categories.json'):
    """
    Orchestrates the categorization process.
    Matches keywords against descriptions and returns the labeled DataFrame.
    """
    df = df.copy()
    df['category'] = 'Other' 
    
    mapping = load_categories(config_path)
    
    for category, keywords in mapping.items():
        if not keywords:
            continue
            
        # Create a regex 'OR' pattern: (keyword1|keyword2|keyword3)
        pattern = '|'.join(map(str, keywords))
        
        # Case-insensitive substring match
        mask = df['description'].str.contains(pattern, case=False, na=False)
        df.loc[mask, 'category'] = category
        
    return df