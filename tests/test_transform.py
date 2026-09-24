import pandas as pd
from src.transform import transform_data, STATUS_MAPPING


def test_status_mapping():
    df = pd.DataFrame({
        "transaction_id": ["TX001", "TX002", "TX003", "TX004"],
        "customer_id": ["C1", "C2", "C3", "C4"],
        "agent_id": ["A1", "A2", "A3", "A4"],
        "transaction_date": ["2026-01-01", "2026-01-01", "2026-01-01", "2026-01-01"],
        "amount": [100, 200, 300, 400],
        "status": ["success", "completed", "pending", "failed"],
    })

    result = transform_data(df)

    assert result.loc[0, "status"] == "SUCCESS"
    assert result.loc[1, "status"] == "SUCCESS"
    assert result.loc[2, "status"] == "PENDING"
    assert result.loc[3, "status"] == "FAILED"


def test_status_mapping_uppercase_input():
    df = pd.DataFrame({
        "transaction_id": ["TX001", "TX002"],
        "customer_id": ["C1", "C2"],
        "agent_id": ["A1", "A2"],
        "transaction_date": ["2026-01-01", "2026-01-01"],
        "amount": [100, 200],
        "status": ["SUCCESS", "PENDING"],
    })

    result = transform_data(df)

    assert result.loc[0, "status"] == "SUCCESS"
    assert result.loc[1, "status"] == "PENDING"


def test_date_conversion():
    df = pd.DataFrame({
        "transaction_id": ["TX001"],
        "customer_id": ["C1"],
        "agent_id": ["A1"],
        "transaction_date": ["2026-07-01"],
        "amount": [100],
        "status": ["success"],
    })

    result = transform_data(df)

    assert pd.api.types.is_datetime64_any_dtype(result["transaction_date"])


def test_amount_conversion():
    df = pd.DataFrame({
        "transaction_id": ["TX001"],
        "customer_id": ["C1"],
        "agent_id": ["A1"],
        "transaction_date": ["2026-07-01"],
        "amount": ["100"],
        "status": ["success"],
    })

    result = transform_data(df)

    assert pd.api.types.is_numeric_dtype(result["amount"])
