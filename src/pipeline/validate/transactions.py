import logging

import pandas as pd

from src.pipeline.contracts import REQUIRED_COLUMNS, FailureReason


def validate_columns(df: pd.DataFrame) -> list:
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    return list(missing)


def validate_nulls(df: pd.DataFrame) -> pd.DataFrame:
    return df[
        df[REQUIRED_COLUMNS]
        .isnull()
        .any(axis=1)
    ]


def validate_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df[
        df.duplicated(subset=["transaction_id"], keep="first")
    ]


def validate_amounts(df: pd.DataFrame) -> pd.DataFrame:
    return df[
        df["amount"] <= 0
    ]


def validate_dates(df: pd.DataFrame) -> pd.DataFrame:
    today = pd.Timestamp.today()
    return df[
        df["transaction_date"] > today
    ]


def run_all_checks(df: pd.DataFrame):
    missing = validate_columns(df)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["failure_reason"] = None

    null_mask = df[REQUIRED_COLUMNS].isnull().any(axis=1)
    df.loc[null_mask, "failure_reason"] = FailureReason.NULL_REQUIRED_FIELD.value

    dup_mask = df.duplicated(subset=["transaction_id"], keep="first")
    df.loc[dup_mask & df["failure_reason"].isna(), "failure_reason"] = FailureReason.DUPLICATE_TRANSACTION.value

    amount_mask = df["amount"] <= 0
    df.loc[amount_mask & df["failure_reason"].isna(), "failure_reason"] = FailureReason.INVALID_AMOUNT.value

    today = pd.Timestamp.today()
    date_mask = df["transaction_date"] > today
    df.loc[date_mask & df["failure_reason"].isna(), "failure_reason"] = FailureReason.INVALID_DATE.value

    invalid_df = df[df["failure_reason"].notna()].copy()
    valid_df = df[df["failure_reason"].isna()].drop(columns=["failure_reason"]).copy()

    logging.info(
        f"Validation complete: {len(valid_df)} valid, {len(invalid_df)} quarantined"
    )

    return valid_df, invalid_df
