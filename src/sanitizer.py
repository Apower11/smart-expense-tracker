import re
import pandas as pd

def clean_data(df):
    """
    Standardizes schema types. 
    Handles locale-specific currency formatting and mixed date strings.
    """
    df = df.copy()
    
    # 1. Clean Dates (US Standard for our integration test)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=False)
    df = df.dropna(subset=['date'])

    # 2. Clean Amounts
    def normalize_amount(val):
        if isinstance(val, (int, float)):
            return float(val)
        
        s = str(val).strip()
        
        # Handle accounting format: (50.00) -> -50.00
        if s.startswith('(') and s.endswith(')'):
            s = '-' + s[1:-1]
        
        # Handle European thousands/decimals: 1.200,50 -> 1200.50
        # If there's a comma and a dot, and the comma comes last, it's Euro-style
        if ',' in s and '.' in s:
            if s.find(',') > s.find('.'):
                s = s.replace('.', '').replace(',', '.')
        elif ',' in s and s.count(',') == 1 and len(s.split(',')[-1]) == 2:
            # Handle case with only a comma: 1200,50 -> 1200.50
            s = s.replace(',', '.')

        # Strip everything except digits, dots, and minus signs
        s = re.sub(r'[^\d.-]', '', s)
        
        try:
            return float(s)
        except ValueError:
            return 0.0

    df['amount'] = df['amount'].apply(normalize_amount)

    df['description'] = df['description'].astype(str).fillna('Unknown')    
    df['description'] = df['description'].str.strip()
    
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