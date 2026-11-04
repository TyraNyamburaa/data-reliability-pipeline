import logging
from typing import Optional

from src.pipeline.config import Settings


def run_spark_streaming_job(
    bootstrap_servers: str,
    topic: str,
    settings: Optional[Settings] = None,
):
    try:
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import from_json, col
        from pyspark.sql.types import StructType, StructField, StringType, DoubleType
    except ImportError:
        logging.error("PySpark is not installed. Install with: pip install pyspark")
        return None

    spark = (
        SparkSession.builder
        .appName("TransactionReliabilityStreaming")
        .getOrCreate()
    )

    schema = StructType([
        StructField("transaction_id", StringType(), True),
        StructField("customer_id", StringType(), True),
        StructField("agent_id", StringType(), True),
        StructField("transaction_date", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("status", StringType(), True),
    ])

    streaming_df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", bootstrap_servers)
        .option("subscribe", topic)
        .option("startingOffsets", "earliest")
        .load()
    )

    parsed_df = streaming_df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    query = (
        parsed_df.writeStream
        .outputMode("append")
        .format("console")
        .start()
    )

    logging.info(f"Streaming job started: consuming from {bootstrap_servers}/{topic}")
    query.awaitTermination(timeout=60)

    spark.stop()
    return query
