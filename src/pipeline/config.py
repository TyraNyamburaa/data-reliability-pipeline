from dataclasses import dataclass
import os
from pathlib import Path

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
        quarantine_path=paths.get("quarantine", os.getenv("QUARANTINE_PATH", "/app/data/quarantine")),
        reports_path=paths.get("reports", "/app/data/reports"),
        config_path=str(path),
    )
