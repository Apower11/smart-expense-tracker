import pytest
import pandas as pd
from src.sanitizer import clean_data

def test_amount_normalization():
    """Verify that varied currency formats become valid floats."""
    data = {
        'amount': ['$1,200.50', '(50.00)', '1.200,50 €', '-$10'],
        'date': ['2026-01-01'] * 4,
        'description': ['test'] * 4
    }
    df = pd.DataFrame(data)
    cleaned_df = clean_data(df)
    
    assert cleaned_df['amount'].iloc[0] == 1200.5
    assert cleaned_df['amount'].iloc[1] == -50.0
    assert cleaned_df['amount'].iloc[3] == -10.0

def test_date_standardization():
    """Verify that different date formats are unified."""
    data = {
        'amount': [10.0] * 3,
        'date': ['2026-01-25', '25/01/2026', 'Jan 25, 2026'],
        'description': ['test'] * 3
    }
    df = pd.DataFrame(data)
    cleaned_df = clean_data(df)
    
    assert cleaned_df['date'].dt.day.unique()[0] == 25
    assert cleaned_df['date'].dt.month.unique()[0] == 1