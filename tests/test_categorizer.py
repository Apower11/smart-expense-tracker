import pytest
import pandas as pd
from src.categorizer import apply_categories

def test_basic_categorization():
    """Verify that keywords map to the correct categories."""
    data = {
        'description': ['Starbucks Coffee', 'Netflix.Com', 'Shell Gas Station'],
        'amount': [5.0, 15.0, 50.0]
    }
    df = pd.DataFrame(data)
    
    # We expect a new 'category' column
    result_df = apply_categories(df)
    
    assert result_df['category'].iloc[0] == 'Dining'
    assert result_df['category'].iloc[1] == 'Entertainment'
    assert result_df['category'].iloc[2] == 'Transport'

def test_fallback_category():
    """Transactions with no matches should be 'Other'."""
    data = {'description': ['Unknown Merchant Ltd'], 'amount': [100.0]}
    df = pd.DataFrame(data)
    
    result_df = apply_categories(df)
    assert result_df['category'].iloc[0] == 'Other'

def test_case_insensitivity():
    """Ensure casing doesn't break the mapping."""
    data = {'description': ['starbucks'], 'amount': [5.0]}
    df = pd.DataFrame(data)
    
    result_df = apply_categories(df)
    assert result_df['category'].iloc[0] == 'Dining'