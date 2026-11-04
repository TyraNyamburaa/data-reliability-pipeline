import pytest
import pandas as pd

from src.pipeline.ingest.batch import load_csv
from src.pipeline.transform.transactions import transform_data, STATUS_MAPPING


def test_status_mapping_values():
    assert STATUS_MAPPING["success"] == "SUCCESS"
    assert STATUS_MAPPING["completed"] == "SUCCESS"
    assert STATUS_MAPPING["pending"] == "PENDING"
    assert STATUS_MAPPING["failed"] == "FAILED"


def test_transform_cleans_columns(tmp_path):
    df = pd.DataFrame({
        "Transaction_ID": ["TX001"],
        "Customer_ID": ["C1"],
        "Agent_ID": ["A1"],
        "Transaction_Date": ["2026-01-01"],
        "Amount": [100],
        "Status": ["SUCCESS"],
    })
    result = transform_data(df)
    assert "transaction_id" in result.columns
    assert "amount" in result.columns


def test_load_csv_missing_file_returns_df(tmp_path):
    df = load_csv(tmp_path / "does_not_exist.csv")
    assert len(df) == 0
