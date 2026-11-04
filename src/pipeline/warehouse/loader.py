import logging
from typing import Optional

from src.pipeline.config import Settings


class CloudWarehouseClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.warehouse_type = settings.warehouse_type

    def load(self, df, table_name: str):
        logging.info(f"Loading to {self.warehouse_type}: reliability.{table_name}")
        if self.warehouse_type == "postgres":
            return self._load_postgres(df, table_name)
        elif self.warehouse_type == "snowflake":
            return self._load_snowflake(df, table_name)
        elif self.warehouse_type == "bigquery":
            return self._load_bigquery(df, table_name)
        elif self.warehouse_type == "redshift":
            return self._load_redshift(df, table_name)
        raise ValueError(f"Unsupported warehouse: {self.warehouse_type}")

    def _load_postgres(self, df, table_name: str):
        from src.pipeline.warehouse.postgres import save_to_postgres
        save_to_postgres(df, self.settings, table_name)
        return True

    def _load_snowflake(self, df, table_name: str):
        logging.info("Snowflake loading configured (placeholder)")
        return True

    def _load_bigquery(self, df, table_name: str):
        logging.info("BigQuery loading configured (placeholder)")
        return True

    def _load_redshift(self, df, table_name: str):
        logging.info("Redshift loading configured (placeholder)")
        return True


def load_to_warehouse(df, settings: Settings, table_name: str):
    client = CloudWarehouseClient(settings)
    return client.load(df, table_name)
