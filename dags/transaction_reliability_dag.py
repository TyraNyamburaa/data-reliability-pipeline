from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/opt/airflow/dags/repo')

from src.pipeline.main import run_pipeline


default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2026, 10, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'transaction_reliability_pipeline',
    default_args=default_args,
    description='Data reliability pipeline for transaction data',
    schedule_interval='@daily',
    catchup=False,
    tags=['transactions', 'reliability', 'data-quality'],
)

run_pipeline_task = PythonOperator(
    task_id='run_pipeline',
    python_callable=run_pipeline,
    dag=dag,
)
