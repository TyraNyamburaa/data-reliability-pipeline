from src.pipeline.ingest.batch import load_csv as load_data, load_all_csvs as load_all_data, validate_schema as validate_columns

REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "agent_id",
    "transaction_date",
    "amount",
    "status",
]
