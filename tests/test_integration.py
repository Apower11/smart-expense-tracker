import pytest
import pandas as pd
import os
from main import run_pipeline

@pytest.fixture
def mock_csv(tmp_path):
    """Creates a raw, messy CSV file for integration testing."""
    csv_file = tmp_path / "raw_data.csv"
    content = (
        "date,amount,description\n"
        "01/25/2026,5.00,Starbucks\n" 
        "01/25/2026,5.00,Starbucks\n"  
        "01/26/2026,15.00,Netflix\n"  
        "02/01/2026,50.00,Unknown\n"   
    )
    csv_file.write_text(content)
    return str(csv_file)

def test_full_pipeline_flow(mock_csv):
    """Ensures data flows through all modules correctly."""
    # Run the orchestrator
    report = run_pipeline(mock_csv)
    
    # 1. Check Deduplication: Starbucks should only be counted once ($5.00)
    # We check the 'Dining' column for the Jan 2026 period
    jan_idx = pd.Period('2026-01', freq='M')
    assert report.loc[jan_idx, 'Dining'] == -5.0
    
    # 2. Check Categorization: Netflix should be Entertainment
    assert report.loc[jan_idx, 'Entertainment'] == -15.0
    
    # 3. Check Date Handling/Aggregation: Unknown should be in February
    feb_idx = pd.Period('2026-02', freq='M')
    assert report.loc[feb_idx, 'Other'] == -50.0

def test_invalid_file_path():
    """Ensure the pipeline raises a helpful error for missing files."""
    with pytest.raises(FileNotFoundError):
        run_pipeline("non_existent_file.csv")