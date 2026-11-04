"""
Airflow DAG definition for the transaction reliability pipeline.
"""

dag_id = "transaction_reliability_batch"
schedule_interval = "@daily"
description = "Orchestrates batch ingestion, validation, quarantine, and reporting"
tasks = ["health_check", "run_pipeline"]
dependencies = {"health_check": ["run_pipeline"]}
