import re
import pandas as pd

def clean_data(df):
    """
    Standardizes schema types. 
    Handles locale-specific currency formatting and mixed date strings.
    """
    df = df.copy() 

    # 1. Cast amounts to float64 using helper
    df['amount'] = df['amount'].apply(parse_amount)

    # 2. Parse dates with 'mixed' to prevent warnings on ambiguous ISO vs localized strings
    df['date'] = pd.to_datetime(
        df['date'], 
        dayfirst=True, 
        errors='coerce', 
        format='mixed'
    )
    
    # 3. Normalize descriptions to Title Case for UI consistency
    df['description'] = df['description'].astype(str).str.strip().str.title()
    
    return df

def parse_amount(val):
    """Internal helper to resolve currency strings and locale decimal logic."""
    if pd.isna(val) or val == '':
        return 0.0
    
    s = str(val).strip()
    
    # Normalize accounting-style negatives: (100.00) -> -100.00
    if s.startswith('(') and s.endswith(')'):
        s = f"-{s[1:-1]}"
        
    # Strip currency symbols/metadata but keep numeric structure (.,-)
    s = re.sub(r'[^\d.,\-]', '', s)
    
    # Heuristic for EU vs US separators: 
    # If comma appears after a dot, or exists without a dot, treat as decimal.
    if ',' in s and ('.' not in s or s.rfind(',') > s.rfind('.')):
        s = s.replace('.', '').replace(',', '.')
    else:
        s = s.replace(',', '')
        
    try:
        return float(s)
    except ValueError:
        return 0.0