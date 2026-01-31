import pandas as pd
import pytest
import os
from src.exporter import export_to_excel

@pytest.fixture
def sample_summary():
    """Create a mock summary pivot table for testing."""
    data = {
        '2026-01': [150.0, -300.0],
        '2026-02': [200.0, -350.0]
    }
    return pd.DataFrame(data, index=['Income', 'Dining'])

@pytest.fixture
def sample_categorized_df():
    """Create a mock categorized dataframe for the Deep Dive section."""
    return pd.DataFrame({
        'date': ['2026-01-25', '2026-01-05', '2026-01-10'],
        'amount': [-1500.00, -1200.00, -45.50],
        'description': ['VIP CONCERT TICKETS', 'Rent', 'Wal-Mart'],
        'category': ['Entertainment', 'Rent', 'Groceries']
    })

def test_excel_export_creates_file(sample_summary, sample_categorized_df, tmp_path):
    output_dir = tmp_path / "reports"
    output_dir.mkdir()

    file_path = export_to_excel(
        summary_df=sample_summary, 
        categorized_df=sample_categorized_df, 
        output_dir=str(output_dir)
    )

    assert os.path.exists(file_path)

def test_excel_content_integrity(sample_summary, sample_categorized_df, tmp_path):
    output_dir = tmp_path / "reports"
    output_dir.mkdir()

    file_path = export_to_excel(
        summary_df=sample_summary, 
        categorized_df=sample_categorized_df, 
        output_dir=str(output_dir)
    )

    read_df = pd.read_excel(file_path, sheet_name='Monthly Summary', index_col=0)
    
    assert "TOTAL INCOME" in read_df.index
    assert "STATUS" in read_df.index