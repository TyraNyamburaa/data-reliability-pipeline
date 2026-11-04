import pandas as pd

STATUS_MAPPING = {
    "success": "SUCCESS",
    "completed": "SUCCESS",
    "done": "SUCCESS",
    "pending": "PENDING",
    "failed": "FAILED",
    "fail": "FAILED",
}


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = df.columns.str.strip().str.lower()

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce",
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    df["status"] = df["status"].astype(str).str.strip().str.lower()

    df["status"] = df["status"].map(STATUS_MAPPING)

    return df
