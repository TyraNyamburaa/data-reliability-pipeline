import logging
from typing import Optional

from src.pipeline.config import Settings
from src.pipeline.validate.transactions import run_all_checks


def run_spark_batch_job(
    file_path: str,
    settings: Optional[Settings] = None,
):
    try:
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import col
    except ImportError:
        logging.error("PySpark is not installed. Install with: pip install pyspark")
        return None

    spark = (
        SparkSession.builder
        .appName("TransactionReliabilityBatch")
        .master("local[*]")
        .getOrCreate()
    )

    df = spark.read.csv(file_path, header=True, inferSchema=True)

    df = df.withColumnRenamed("transaction_date", "transaction_date")
    df = df.filter(col("amount") > 0)

    valid_df = df.filter(
        col("transaction_id").isNotNull()
        & col("customer_id").isNotNull()
        & col("amount").isNotNull()
        & col("transaction_date").isNotNull()
    )

    valid_count = valid_df.count()
    total_count = df.count()

    logging.info(f"Spark batch job complete: {valid_count}/{total_count} valid")

    spark.stop()
    return valid_count, total_count
