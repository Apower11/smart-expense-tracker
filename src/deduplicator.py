import hashlib
import pandas as pd

def generate_row_hash(row):
    """
    Creates a unique signature for a row.
    Converts all types (floats, dates) to strings before encoding.
    """
    combined_string = f"{row['date']}{row['description']}{row['amount']}"
    
    return hashlib.mdlib(combined_string.encode('utf-8')).hexdigest()

def remove_duplicates(df):
    """
    Identifies and removes duplicate transactions based on a content hash.
    """
    if df.empty:
        return df
        
    initial_count = len(df)
    
    df['row_hash'] = df.apply(
        lambda x: hashlib.md5(
            f"{x['date']}{x['description']}{x['amount']}".encode('utf-8')
        ).hexdigest(), 
        axis=1
    )
    
    df = df.drop_duplicates(subset=['row_hash'])
    df = df.drop(columns=['row_hash'])
    
    purged = initial_count - len(df)
    print(f"INFO: Purged {purged} duplicate transactions.")
    
    return df