import logging
from typing import Optional

from src.pipeline.config import Settings, load_settings


def run_spark_streaming_job(
    bootstrap_servers: str = "localhost:9092",
    topic: str = "transactions.raw",
    settings: Optional[Settings] = None,
):
    try:
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import from_json, col, when
        from pyspark.sql.types import StructType, StructField, StringType, DoubleType
    except ImportError:
        logging.error("PySpark is not installed. Install with: pip install pyspark")
        return None

    if settings is None:
        settings = load_settings()

    spark = (
        SparkSession.builder
        .appName("TransactionReliabilityStreaming")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )

    schema = StructType([
        StructField("transaction_id", StringType(), True),
        StructField("customer_id", StringType(), True),
        StructField("agent_id", StringType(), True),
        StructField("region", StringType(), True),
        StructField("transaction_date", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("currency", StringType(), True),
        StructField("status", StringType(), True),
        StructField("payment_method", StringType(), True),
        StructField("event_time", StringType(), True),
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

    validated_df = parsed_df.withColumn(
        "validation_result",
        when(
            col("transaction_id").isNotNull() & col("amount").isNotNull() & (col("amount") > 0),
            "VALID",
        ).otherwise("INVALID"),
    )

    query = (
        validated_df.writeStream
        .outputMode("append")
        .format("console")
        .start()
    )

    logging.info(f"Streaming job started: consuming from {bootstrap_servers}/{topic}")
    return query
