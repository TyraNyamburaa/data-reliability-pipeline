import logging

from src.pipeline.config import load_settings
from src.pipeline.ingest.batch import load_all_csvs
from src.pipeline.transform.transactions import transform_data
from src.pipeline.validate.transactions import run_all_checks
from src.pipeline.warehouse.postgres import save_clean_data, save_quarantine_data, save_to_postgres
from src.pipeline.reporting.quality_report import generate_quality_report
from src.pipeline.logging import logger

REPORT_PATH = "data/reports/summary_report.json"


def run_pipeline():
    settings = load_settings()
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    logger.info("pipeline.start")

    logger.info("step.load_raw")
    df = load_all_csvs(settings.input_path)

    if df.empty:
        logger.warning("pipeline.no_data")
        return None

    logger.info("step.transform")
    df = transform_data(df)

    logger.info("step.validate")
    valid_df, invalid_df = run_all_checks(df)
    logger.info(f"validation.results valid={len(valid_df)} quarantined={len(invalid_df)}")

    logger.info("step.save_local")
    save_clean_data(valid_df, settings)
    save_quarantine_data(invalid_df, settings)

    logger.info("step.save_postgres")
    try:
        save_to_postgres(valid_df, settings, "clean_transactions", if_exists="append")
        save_to_postgres(invalid_df, settings, "quarantine", if_exists="append")
    except Exception as e:
        logger.warning(f"postgres.save.failed error={e}")

    logger.info("step.generate_report")
    report = generate_quality_report(valid_df, invalid_df, REPORT_PATH)
    logger.info("pipeline.complete")
    return report


if __name__ == "__main__":
    run_pipeline()
