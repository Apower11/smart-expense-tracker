import pytest
import pandas as pd
from src.reporter import summarize_by_month

@pytest.fixture
def categorized_data():
    """Provides a mix of dates and categories for aggregation testing."""
    return pd.DataFrame({
        'date': pd.to_datetime([
            '2026-01-05', '2026-01-15', 
            '2026-01-20',               
            '2026-02-05',               
            '2026-02-10'                
        ]),
        'amount': [10.0, 20.0, 50.0, 15.0, 100.0],
        'category': ['Dining', 'Dining', 'Transport', 'Dining', 'Other']
    })

def test_monthly_totals(categorized_data):
    """Check if math adds up correctly per month per category."""
    summary = summarize_by_month(categorized_data)
    
    # Check January Dining (10 + 20 = 30)
    # Note: Summary index will likely be the Month period
    jan_idx = pd.Period('2026-01', freq='M')
    assert summary.loc[jan_idx, 'Dining'] == 30.0
    
    # Check February Dining
    feb_idx = pd.Period('2026-02', freq='M')
    assert summary.loc[feb_idx, 'Dining'] == 15.0

def test_missing_category_is_zero(categorized_data):
    """If a category has no spend in a month, it should be 0.0, not NaN."""
    summary = summarize_by_month(categorized_data)
    
    feb_idx = pd.Period('2026-02', freq='M')
    # Transport has no spend in Feb
    assert summary.loc[feb_idx, 'Transport'] == 0.0