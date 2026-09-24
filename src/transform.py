# Here we convert the ingested data into a format that can be used for further processing and analysis. This may involve cleaning, transforming, and structuring the data as needed.
import pandas as pd

STATUS_MAPPING = {
    "success": "SUCCESS",
    "completed": "SUCCESS",
    "done": "SUCCESS",
    "pending": "PENDING",
    "failed": "FAILED",
    "fail": "FAILED"
}

def transform_data(df):
    df = df.copy()  # Avoid modifying the original DataFrame

    # Standardize the 'status' column
    df.columns = (
        df.columns
        .str.strip()  # Remove leading/trailing whitespace
        .str.lower()  # Convert to lowercase
    )

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"], 
        errors="coerce"
    )

    # Map the amount values to standardized values
    df["amount"] = pd.to_numeric(
        df["amount"], 
        errors="coerce"
    )

    # Standardize the 'status' column using the mapping
    df["status"] = (
        df["status"]
        .astype(str)  # Ensure the status is a string
        .str.strip()  # Remove leading/trailing whitespace
        .str.lower()  # Convert to lowercase
    )

    df["status"] = df["status"].map(STATUS_MAPPING)

    return df