from dataclasses import dataclass
import os


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

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

def load_settings() -> Settings:
    return Settings(
        pipeline_env=os.getenv("PIPELINE_ENV", "local"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        postgres_host=os.getenv("POSTGRES_HOST", "localhost"),
        postgres_port=int(os.getenv("POSTGRES_PORT", "5432")),
        postgres_db=os.getenv("POSTGRES_DB", "transaction_warehouse"),
        postgres_user=os.getenv("POSTGRES_USER", "pipeline_user"),
        postgres_password=os.getenv("POSTGRES_PASSWORD", ""),
        input_path=os.getenv("INPUT_PATH", "data/raw"),
        processed_path=os.getenv("PROCESSED_PATH", "data/processed"),
        quarantine_path=os.getenv("QUARANTINE_PATH", "data/quarantine"),
    )