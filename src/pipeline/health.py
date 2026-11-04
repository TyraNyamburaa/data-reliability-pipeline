from src.pipeline.config import load_settings
from src.pipeline.logging import logger


def health_check() -> dict:
    settings = load_settings()
    return {
        "status": "ok",
        "env": settings.pipeline_env,
        "postgres_host": settings.postgres_host,
        "postgres_port": settings.postgres_port,
        "raw_path": settings.input_path,
        "processed_path": settings.processed_path,
        "quarantine_path": settings.quarantine_path,
    }


if __name__ == "__main__":
    logger.info("Running pipeline health check")
    result = health_check()
    logger.info(f"Health check result: {result}")
    print(result)
