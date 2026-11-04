import logging
import sys
from pathlib import Path

from src.pipeline.config import load_settings
from src.pipeline.ingest.batch import load_all_csvs
from src.pipeline.transform.transactions import transform_data
from src.pipeline.validate.transactions import run_all_checks
from src.pipeline.warehouse.postgres import save_clean_data, save_quarantine_data, save_to_postgres
from src.pipeline.reporting.quality_report import generate_quality_report

REPORT_PATH = "data/reports/summary_report.json"


def run_pipeline():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    settings = load_settings()

    logging.info("Step 1: Load raw data")
    df = load_all_csvs(settings.input_path)

    if df.empty:
        logging.warning("No raw data found. Pipeline exiting.")
        return None

    logging.info(f"Loaded {len(df)} raw records")

    logging.info("Step 2: Transform data")
    df = transform_data(df)

    logging.info("Step 3: Validate data")
    valid_df, invalid_df = run_all_checks(df)

    logging.info("Step 4: Save clean and quarantine data")
    save_clean_data(valid_df, settings)
    save_quarantine_data(invalid_df, settings)

    logging.info("Step 5: Save to PostgreSQL")
    try:
        save_to_postgres(valid_df, settings, "clean_transactions", if_exists="append")
        save_to_postgres(invalid_df, settings, "quarantine", if_exists="append")
    except Exception as e:
        logging.warning(f"Could not write to PostgreSQL: {e}")
        logging.info("Clean and quarantine CSVs have already been written locally.")

    logging.info("Step 6: Generate quality report")
    report = generate_quality_report(valid_df, invalid_df, REPORT_PATH)

    logging.info("Pipeline complete.")
    return report


if __name__ == "__main__":
    run_pipeline()
