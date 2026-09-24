import pandas as pd
import logging
from pathlib import Path
import glob


def load_data(file_path: str) -> pd.DataFrame:
    logging.info(f"Loading file: {file_path}")

    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        logging.warning(f"File {file_path} is empty. Skipping.")
        return pd.DataFrame()

    logging.info(f"Loaded {len(df)} records from {file_path}")

    return df


def load_all_data(directory: str) -> pd.DataFrame:
    directory_path = Path(directory)
    files = sorted(glob.glob(str(directory_path / "*.csv")))

    if not files:
        logging.warning(f"No CSV files found in {directory}")
        return pd.DataFrame()

    dfs = []
    for file_path in files:
        df = load_data(file_path)
        if not df.empty:
            dfs.append(df)

    if dfs:
        combined = pd.concat(dfs, ignore_index=True)
        logging.info(f"Combined {len(combined)} records from {len(dfs)} files")
        return combined

    return pd.DataFrame()
