import hashlib
import pandas as pd

def remove_duplicates(df):
    """
    Identifies and removes duplicate transactions.
    Creates a 'fingerprint' hash based on date, amount, and description.
    """
    if df.empty:
        return df

    df = df.copy()

    # Create a unique string for each row to hash
    # Using .dt.date ensures time-of-day doesn't break the match
    fingerprint_source = (
        df['date'].dt.date.astype(str) + 
        df['amount'].astype(str) + 
        df['description'].str.upper()
    )

    # Generate MD5 hashes for each transaction
    df['transaction_id'] = [
        hashlib.md5(val.encode()).hexdigest() for val in fingerprint_source
    ]

    # Drop duplicates, keeping the first occurrence
    initial_count = len(df)
    df = df.drop_duplicates(subset=['transaction_id'], keep='first')
    
    removed = initial_count - len(df)
    if removed > 0:
        print(f"INFO: Purged {removed} duplicate transactions.")

    # Drop the temporary ID before returning (optional, or keep it as a Primary Key)
    return df.drop(columns=['transaction_id'])