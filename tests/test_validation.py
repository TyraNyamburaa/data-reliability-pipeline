import pandas as pd
import pytest
from src.validation import (
    run_all_checks,
    validate_duplicates,
    validate_amounts,
    validate_nulls,
    validate_dates,
    validate_columns,
)


def test_duplicate_detection():
    df = pd.DataFrame({
        "transaction_id": ["TX001", "TX001", "TX002", "TX003"],
        "customer_id": ["C1", "C1", "C2", "C3"],
        "agent_id": ["A1", "A1", "A2", "A3"],
        "transaction_date": pd.to_datetime(["2026-01-01", "2026-01-01", "2026-01-01", "2026-01-01"]),
        "amount": [100, 100, 200, 300],
        "status": ["SUCCESS", "SUCCESS", "PENDING", "FAILED"],
    })

    duplicates = validate_duplicates(df)

    assert len(duplicates) == 1
    assert duplicates.iloc[0]["transaction_id"] == "TX001"


def test_invalid_amount():
    df = pd.DataFrame({
        "transaction_id": ["TX001", "TX002", "TX003"],
        "customer_id": ["C1", "C2", "C3"],
        "agent_id": ["A1", "A2", "A3"],
        "transaction_date": pd.to_datetime(["2026-01-01", "2026-01-01", "2026-01-01"]),
        "amount": [100, -50, 0],
        "status": ["SUCCESS", "PENDING", "FAILED"],
    })

    invalid = validate_amounts(df)

    assert len(invalid) == 2
    assert invalid.iloc[0]["amount"] == -50
    assert invalid.iloc[1]["amount"] == 0


def test_null_detection():
    df = pd.DataFrame({
        "transaction_id": ["TX001", "TX002"],
        "customer_id": ["C1", None],
        "agent_id": ["A1", "A2"],
        "transaction_date": pd.to_datetime(["2026-01-01", None]),
        "amount": [100, 200],
        "status": ["SUCCESS", "PENDING"],
    })

    nulls = validate_nulls(df)

    assert len(nulls) == 1
    assert nulls.iloc[0]["transaction_id"] == "TX002"


def test_invalid_date():
    future_date = pd.Timestamp.today() + pd.Timedelta(days=30)
    df = pd.DataFrame({
        "transaction_id": ["TX001", "TX002"],
        "customer_id": ["C1", "C2"],
        "agent_id": ["A1", "A2"],
        "transaction_date": pd.to_datetime(["2026-01-01", future_date]),
        "amount": [100, 200],
        "status": ["SUCCESS", "PENDING"],
    })

    invalid = validate_dates(df)

    assert len(invalid) == 1
    assert invalid.iloc[0]["transaction_id"] == "TX002"


def test_run_all_checks_quarantine():
    df = pd.DataFrame({
        "transaction_id": ["TX001", "TX001", "TX002", "TX003"],
        "customer_id": ["C1", "C1", "C2", "C3"],
        "agent_id": ["A1", "A1", "A2", "A3"],
        "transaction_date": pd.to_datetime(["2026-01-01", "2026-01-01", "2026-01-01", "2026-01-01"]),
        "amount": [100, 100, -50, 200],
        "status": ["SUCCESS", "SUCCESS", "PENDING", "FAILED"],
    })

    valid_df, invalid_df = run_all_checks(df)

    assert len(valid_df) == 2
    assert len(invalid_df) == 2
    assert "failure_reason" in invalid_df.columns


def test_missing_columns():
    df = pd.DataFrame({"transaction_id": ["TX001"], "amount": [100]})

    missing = validate_columns(df)

    assert len(missing) == 4
    assert "customer_id" in missing
