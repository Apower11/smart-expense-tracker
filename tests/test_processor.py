import pytest
import pathlib
import pandas as pd
from src.processor import load_data

# Set up the path to your fixtures
FIXTURE_DIR = pathlib.Path(__file__).parent / "fixtures"

# --- CATEGORY 1: FILES THAT MUST PASS ---
# These files have different quirks but should result in a valid 3-column DataFrame
PASS_FILES = [
    "standard_pass.csv",
    "dirty_formatting.csv",
    "mixed_date_formats.csv",
    "duplicate_entries.csv",
    "encoding_differences.csv",
    "non_numeric_amount.csv",
    "outlier.csv",
    "html_injection_desc.csv",
    "multi_line_descriptions.csv",
    "european_separator.csv",
    "bom_encoding.csv",
    "mixed_currency_symbols.csv",
    "accent_marks_utf8.csv",
    "non_latin_scripts.csv",
    "rtl_text_alignment.csv",
    "mixed_language_normalization.csv",
    "wide_metadata.csv",
    "mega_wide.csv",
    "skyscraper_deep.csv",
    "horizon_wide.csv",
    "block_big.csv",
    "sparse_big.csv"
]

@pytest.mark.parametrize("filename", PASS_FILES)
def test_loader_should_pass(filename):
    """Verifies that all 'valid-but-quirky' files are ingested without crashing."""
    file_path = FIXTURE_DIR / filename
    
    # Check if the volumetric files exist (since they aren't in Git)
    if not file_path.exists():
        pytest.skip(f"Large file {filename} not generated. Run generator first.")

    df = load_data(file_path)
    
    # 1. Check structure
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    
    # 2. Check column normalization (Must be 3 specific columns)
    expected_cols = {'date', 'description', 'amount'}
    assert set(df.columns) == expected_cols
    assert df.shape[1] == 3

# --- CATEGORY 2: FILES THAT MUST FAIL ---
# These are 'poison' files that should raise specific errors
FAIL_CASES = [
    ("empty.csv", ValueError),
    ("zero_byte_file.csv", ValueError),
    ("wrong_file_type.jar", ValueError),
    ("wrong_columns.csv", KeyError),
]

@pytest.mark.parametrize("filename, expected_error", FAIL_CASES)
def test_loader_should_fail(filename, expected_error):
    """Verifies that the loader correctly rejects bad data with the right error type."""
    file_path = FIXTURE_DIR / filename
    
    with pytest.raises(expected_error):
        load_data(file_path)

# --- CATEGORY 3: SPECIAL CASES ---
def test_schema_mapping_spanish():
    """Verify that we can handle non-English column headings."""
    file_path = FIXTURE_DIR / "column_headings_different_language.csv"
    # Note: This might require your load_data to have a mapper 
    # For now, we expect it to fail unless we've implemented the mapper
    with pytest.raises(KeyError):
        load_data(file_path)