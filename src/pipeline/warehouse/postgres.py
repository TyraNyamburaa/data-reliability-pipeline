import json
import logging
from pathlib import Path
from typing import Dict

import pandas as pd
from sqlalchemy import create_engine, text


def save_clean_data(df: pd.DataFrame, settings) -> str:
    if df.empty:
        logging.warning("No clean records to save")
        return ""

    path = Path(settings.processed_path)
    path.mkdir(parents=True, exist_ok=True)

    output_path = path / "clean_transactions.csv"
    df.to_csv(output_path, index=False)
    logging.info(f"Saved {len(df)} clean records to {output_path}")
    return str(output_path)


def save_quarantine_data(df: pd.DataFrame, settings) -> str:
    if df.empty:
        logging.warning("No quarantined records to save")
        return ""

    path = Path(settings.quarantine_path)
    path.mkdir(parents=True, exist_ok=True)

    output_path = path / "invalid_transactions.csv"
    df.to_csv(output_path, index=False)
    logging.info(f"Saved {len(df)} quarantined records to {output_path}")
    return str(output_path)


def save_to_postgres(
    df: pd.DataFrame,
    settings,
    table_name: str,
    if_exists: str = "append",
) -> None:
    engine = create_engine(settings.database_url)
    df.to_sql(
        name=table_name,
        con=engine,
        schema="reliability",
        if_exists=if_exists,
        index=False,
    )
    engine.dispose()
    logging.info(f"Wrote {len(df)} records to reliability.{table_name}")


def load_quarantine_from_postgres(settings) -> pd.DataFrame:
    engine = create_engine(settings.database_url)
    query = text('SELECT * FROM reliability.quarantine ORDER BY created_at DESC')
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    engine.dispose()
    return df
