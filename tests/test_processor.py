import pytest
import pathlib
import pandas as pd
from src.processor import load_data

# Project-level paths
BASE_DIR = pathlib.Path(__file__).parent
FIXTURE_DIR = BASE_DIR / "fixtures"

# --- Test Case Definitions ---

# Files that should be handled gracefully by the loader
STRESS_TEST_FILES = [
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
    "sparse_big.csv"
]

# Files that are expected to trigger specific exceptions
FAILURE_SCENARIOS = [
    ("empty.csv", ValueError),
    ("zero_byte_file.csv", ValueError),
    ("wrong_file_type.jar", ValueError),
    ("wrong_columns.csv", KeyError),
]

# --- Test Implementations ---

@pytest.mark.parametrize("filename", STRESS_TEST_FILES)
def test_ingestion_integrity(filename):
    """Ensure various edge-case files result in a valid 3-column schema."""
    target_path = FIXTURE_DIR / filename
    
    if not target_path.exists():
        pytest.skip(f"Target {filename} not found locally. Skipping.")

    result_df = load_data(target_path)
    
    # Validation assertions
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty
    assert result_df.shape[1] == 3
    
    # Standardized header check
    expected_headers = {'date', 'description', 'amount'}
    assert set(result_df.columns) == expected_headers


@pytest.mark.parametrize("filename, error_type", FAILURE_SCENARIOS)
def test_input_validation(filename, error_type):
    """Verify core validation rules for malformed or invalid inputs."""
    target_path = FIXTURE_DIR / filename
    
    with pytest.raises(error_type):
        load_data(target_path)


def test_unsupported_language_headers():
    """Confirms current limitation: non-English headers should fail until mapper is implemented."""
    target_path = FIXTURE_DIR / "column_headings_different_language.csv"
    
    if not target_path.exists():
        pytest.skip("Spanish/International fixture missing.")

    with pytest.raises(KeyError):
        load_data(target_path)