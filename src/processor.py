import pandas as pd
import pathlib
import csv

def load_data(file_path, chunk_size=20000):
    path = pathlib.Path(file_path)
    
    # --- Initial Validation ---
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")
    if path.suffix.lower() != '.csv':
        raise ValueError(f"Expected .csv, got {path.suffix}")
    if path.stat().st_size == 0:
        raise ValueError("File is 0 bytes")

    # --- Dialect & Encoding Detection ---
    # Sniff first 4KB to handle European (;) vs US (,) delimiters and BOMs
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            sample = f.read(4096)
            if not sample.strip():
                raise ValueError("File is whitespace or empty headers")
            
            dialect = csv.Sniffer().sniff(sample)
            sep = dialect.delimiter
        encoding = 'utf-8-sig'
    except (csv.Error, UnicodeDecodeError):
        # Fallback for non-standard encodings (e.g. Excel exports)
        sep = None 
        encoding = 'latin1'

    # --- Stream Processing ---
    try:
        reader = pd.read_csv(
            file_path,
            sep=sep,
            encoding=encoding,
            engine='python',
            on_bad_lines='warn',
            chunksize=chunk_size
        )
        
        required_cols = {'date', 'description', 'amount'}
        processed = []
        
        for chunk in reader:
            # Column cleanup: normalize to lowercase and strip whitespace
            chunk.columns = [str(c).strip().lower() for c in chunk.columns]
            
            if not required_cols.issubset(chunk.columns):
                missing = required_cols - set(chunk.columns)
                raise KeyError(f"Missing required columns: {missing}")
            
            # Filter columns immediately to keep memory usage low
            processed.append(chunk[list(required_cols)])
            
        if not processed:
            raise ValueError("No valid data rows found")
            
        full_df = pd.concat(processed, ignore_index=True)
        
        if full_df.empty:
            raise ValueError("Dataset is empty after processing")
            
        return full_df

    except Exception as e:
        # Re-raise known logic errors; wrap unknown parser crashes in IOError
        if isinstance(e, (KeyError, ValueError)):
            raise
        raise IOError(f"Failed to parse CSV: {e}")