import logging
from typing import Optional

from src.pipeline.config import Settings, load_settings


def run_spark_batch_job(
    file_path: Optional[str] = None,
    settings: Optional[Settings] = None,
):
    try:
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import col, lower, to_date, trim
    except ImportError:
        logging.error("PySpark is not installed. Install with: pip install pyspark")
        return None

    if settings is None:
        settings = load_settings()

    if file_path is None:
        file_path = f"{settings.input_path}/transactions_2026_01.csv"

    spark = (
        SparkSession.builder.appName("TransactionReliabilityBatch")
        .master("local[*]")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )

    df = spark.read.csv(file_path, header=True, inferSchema=True)
    df = df.withColumnRenamed("Transaction_ID", "transaction_id")

    transformed = (
        df.withColumn("status_clean", lower(trim(col("status"))))
        .withColumn("transaction_date_parsed", to_date(col("transaction_date")))
        .withColumn("amount_numeric", col("amount").cast("double"))
    )

    valid_df = transformed.filter(
        col("transaction_id").isNotNull() & col("customer_id").isNotNull() & col("amount_numeric")
        > 0 & col("transaction_date_parsed").isNotNull()
    )

    total_count = df.count()
    valid_count = valid_df.count()

    logging.info(f"Spark batch job complete: {valid_count}/{total_count} valid records")

    spark.stop()
    return {"total": total_count, "valid": valid_count}
