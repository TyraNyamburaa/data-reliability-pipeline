"""
Airflow DAG for orchestrating the transaction reliability batch pipeline.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.pipeline.main import run_pipeline
from src.pipeline.health import health_check


default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "start_date": datetime(2026, 10, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="transaction_reliability_batch",
    default_args=default_args,
    description="Batch orchestration for transaction data reliability pipeline",
    schedule_interval="@daily",
    catchup=False,
    tags=["transactions", "reliability", "batch"],
    max_active_runs=1,
) as dag:
    check_health = PythonOperator(
        task_id="health_check",
        python_callable=health_check,
    )

    run_batch_pipeline = PythonOperator(
        task_id="run_pipeline",
        python_callable=run_pipeline,
    )

    check_health >> run_batch_pipeline
