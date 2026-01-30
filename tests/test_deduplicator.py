import pytest
import pandas as pd
from src.deduplicator import remove_duplicates

def test_exact_deduplication():
    """Ensure identical rows are collapsed into one."""
    data = {
        'date': ['2026-01-25', '2026-01-25'],
        'amount': [50.0, 50.0],
        'description': ['Starbucks', 'Starbucks']
    }
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    deduped_df = remove_duplicates(df)
    assert len(deduped_df) == 1

def test_different_transactions_preserved():
    """Ensure unique transactions with same amount/date aren't accidentally deleted."""
    data = {
        'date': ['2026-01-25', '2026-01-25'],
        'amount': [12.0, 12.0],
        'description': ['App Store', 'Netflix']
    }
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    deduped_df = remove_duplicates(df)
    assert len(deduped_df) == 2