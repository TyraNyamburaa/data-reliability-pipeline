import logging
from pathlib import Path

from src.ingest import load_all_data
from src.transform import transform_data
from src.validation import run_all_checks
from src.report import generate_report, save_report, build_failure_breakdown


RAW_DIR = Path("data/raw")
CLEAN_OUTPUT = Path("data/clean/clean_transactions.csv")
QUARANTINE_OUTPUT = Path("data/quarantine/invalid_transactions.csv")
REPORT_OUTPUT = Path("data/reports/summary_report.json")


def save_clean_data(valid_df, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    valid_df.to_csv(path, index=False)
    return path


def save_quarantine_data(invalid_df, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    invalid_df.to_csv(path, index=False)
    return path


def run_pipeline(
    input_dir=RAW_DIR,
    clean_output=CLEAN_OUTPUT,
    quarantine_output=QUARANTINE_OUTPUT,
    report_output=REPORT_OUTPUT,
):
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    logging.info("Step 1: Load raw data")
    df = load_all_data(str(input_dir))
    if df.empty:
        logging.warning("No raw data found. Pipeline exiting.")
        return None

    logging.info(f"Loaded {len(df)} raw records")

    logging.info("Step 2: Transform data")
    df = transform_data(df)

    logging.info("Step 3: Validate data")
    valid_df, invalid_df = run_all_checks(df)

    logging.info(f"Valid records: {len(valid_df)}")
    logging.info(f"Invalid records: {len(invalid_df)}")

    logging.info("Step 4: Save clean data")
    save_clean_data(valid_df, str(clean_output))

    logging.info("Step 5: Save quarantine data")
    save_quarantine_data(invalid_df, str(quarantine_output))

    logging.info("Step 6: Generate report")
    failure_breakdown = build_failure_breakdown(invalid_df)
    report = generate_report(
        total=len(df),
        passed=len(valid_df),
        failed=len(invalid_df),
        failures=failure_breakdown,
    )
    save_report(report, str(report_output))

    logging.info("Pipeline complete.")
    return report


if __name__ == "__main__":
    run_pipeline()
