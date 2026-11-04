import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


@dataclass(frozen=True)
class Settings:
    pipeline_env: str
    log_level: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    input_path: str
    processed_path: str
    quarantine_path: str
    reports_path: str
    config_path: str
    warehouse_type: str = "postgres"
    snowflake_account: Optional[str] = None
    snowflake_user: Optional[str] = None
    snowflake_password: Optional[str] = None
    snowflake_database: Optional[str] = None
    snowflake_warehouse: Optional[str] = None
    snowflake_schema: Optional[str] = None
    bigquery_project_id: Optional[str] = None
    bigquery_dataset: Optional[str] = None
    bigquery_credentials_path: Optional[str] = None
    redshift_host: Optional[str] = None
    redshift_port: Optional[int] = None
    redshift_database: Optional[str] = None
    redshift_user: Optional[str] = None
    redshift_password: Optional[str] = None

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


def _substitute_env_vars(obj):
    if isinstance(obj, dict):
        return {k: _substitute_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_substitute_env_vars(v) for v in obj]
    elif isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
        inner = obj[2:-1]
        if ":-" in inner:
            key, default = inner.split(":-", 1)
            return os.getenv(key, default)
        return os.getenv(inner, obj)
    return obj


def load_settings(config_path: str = "config/pipeline.yaml") -> Settings:
    config = {}
    path = Path(config_path)
    if path.exists():
        with open(path) as f:
            raw = yaml.safe_load(f) or {}
        config = _substitute_env_vars(raw)

    paths = config.get("paths", {})
    postgres = config.get("postgres", {})
    snowflake = config.get("snowflake", {})
    bigquery = config.get("bigquery", {})
    redshift = config.get("redshift", {})

    return Settings(
        pipeline_env=config.get("env", os.getenv("PIPELINE_ENV", "local")),
        log_level=config.get("log_level", os.getenv("LOG_LEVEL", "INFO")),
        postgres_host=postgres.get("host", os.getenv("POSTGRES_HOST", "postgres")),
        postgres_port=int(postgres.get("port", os.getenv("POSTGRES_PORT", "5432"))),
        postgres_db=postgres.get("database", os.getenv("POSTGRES_DB", "transaction_warehouse")),
        postgres_user=postgres.get("user", os.getenv("POSTGRES_USER", "pipeline_user")),
        postgres_password=postgres.get("password", os.getenv("POSTGRES_PASSWORD", "")),
        input_path=paths.get("raw", os.getenv("INPUT_PATH", "/app/data/raw")),
        processed_path=paths.get("processed", os.getenv("PROCESSED_PATH", "/app/data/processed")),
        quarantine_path=paths.get(
            "quarantine", os.getenv("QUARANTINE_PATH", "/app/data/quarantine")
        ),
        reports_path=paths.get("reports", "/app/data/reports"),
        config_path=str(path),
        warehouse_type=config.get("warehouse_type", os.getenv("WAREHOUSE_TYPE", "postgres")),
        snowflake_account=snowflake.get("account") or os.getenv("SNOWFLAKE_ACCOUNT"),
        snowflake_user=snowflake.get("user") or os.getenv("SNOWFLAKE_USER"),
        snowflake_password=snowflake.get("password") or os.getenv("SNOWFLAKE_PASSWORD"),
        snowflake_database=snowflake.get("database") or os.getenv("SNOWFLAKE_DATABASE"),
        snowflake_warehouse=snowflake.get("warehouse") or os.getenv("SNOWFLAKE_WAREHOUSE"),
        snowflake_schema=snowflake.get("schema") or os.getenv("SNOWFLAKE_SCHEMA"),
        bigquery_project_id=bigquery.get("project_id") or os.getenv("BIGQUERY_PROJECT_ID"),
        bigquery_dataset=bigquery.get("dataset") or os.getenv("BIGQUERY_DATASET"),
        bigquery_credentials_path=bigquery.get("credentials_path")
        or os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        redshift_host=redshift.get("host") or os.getenv("REDSHIFT_HOST"),
        redshift_port=int(redshift.get("port", 5439)) if redshift.get("port") else None,
        redshift_database=redshift.get("database") or os.getenv("REDSHIFT_DATABASE"),
        redshift_user=redshift.get("user") or os.getenv("REDSHIFT_USER"),
        redshift_password=redshift.get("password") or os.getenv("REDSHIFT_PASSWORD"),
    )
