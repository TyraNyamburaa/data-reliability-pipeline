from datetime import datetime
import pandas as pd

REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "agent_id",
    "transaction_date",
    "amount",
    "status"
]

FAILURE_NULL = "NULL_REQUIRED_FIELD"
FAILURE_DUPLICATE = "DUPLICATE_TRANSACTION"
FAILURE_AMOUNT = "INVALID_AMOUNT"
FAILURE_DATE = "INVALID_DATE"


def validate_columns(df):
    missing = set(REQUIRED_COLUMNS) - set(df.columns)

    return list(missing)


def validate_nulls(df):

    return df[
        df[REQUIRED_COLUMNS]
        .isnull()
        .any(axis=1)
    ]


def validate_duplicates(df):
    return df[
        df.duplicated(subset=["transaction_id"], keep="first")
    ]


def validate_amounts(df):
    return df[
        df["amount"] <= 0
    ]


def validate_dates(df):

    today = pd.Timestamp.today()

    return df[
        (df["transaction_date"] > today)
    ]


def run_all_checks(df):
    missing = validate_columns(df)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["failure_reason"] = None

    null_mask = df[REQUIRED_COLUMNS].isnull().any(axis=1)
    df.loc[null_mask, "failure_reason"] = FAILURE_NULL

    dup_mask = df.duplicated(subset=["transaction_id"], keep="first")
    df.loc[dup_mask & df["failure_reason"].isna(), "failure_reason"] = FAILURE_DUPLICATE

    amount_mask = df["amount"] <= 0
    df.loc[amount_mask & df["failure_reason"].isna(), "failure_reason"] = FAILURE_AMOUNT

    today = pd.Timestamp.today()
    date_mask = df["transaction_date"] > today
    df.loc[date_mask & df["failure_reason"].isna(), "failure_reason"] = FAILURE_DATE

    invalid_df = df[df["failure_reason"].notna()].copy()
    valid_df = df[df["failure_reason"].isna()].drop(columns=["failure_reason"]).copy()

    return valid_df, invalid_df
