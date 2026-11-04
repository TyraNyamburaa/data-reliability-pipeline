# Data Reliability Pipeline

A data reliability pipeline that ingests raw transaction CSV files, transforms and validates the data, quarantines invalid records (instead of deleting them), and generates a data quality report.

## Quick Start with Docker (Recommended)

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Start all services:
   ```bash
   docker compose up --build
   ```

3. Stop all services:
   ```bash
   docker compose down
   ```

4. Stop all services and delete local database data (destructive):
   ```bash
   docker compose down -v
   ```

## Local Development (Without Docker)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the tests:
   ```bash
   python -m pytest tests/ -v
   ```

3. Run the pipeline:
   ```bash
   python -m src.pipeline.main
   ```

## Debugging

View logs from the services:
```bash
docker compose logs postgres
docker compose logs pipeline
```

## Architecture

The pipeline follows a 6-step flow:
```
Raw Data → Ingestion → Transformation → Validation → Clean/Quarantine Storage → Report
```

## Validation Rules

| Rule | Check | Failure Code |
|------|-------|--------------|
| Required Columns | All columns in REQUIRED_COLUMNS present | N/A (raises error) |
| Null Fields | No nulls in required columns | `NULL_REQUIRED_FIELD` |
| Duplicates | transaction_id must be unique | `DUPLICATE_TRANSACTION` |
| Amount | amount > 0 | `INVALID_AMOUNT` |
| Future Date | transaction_date <= today | `INVALID_DATE` |

## Outputs

- `data/processed/clean_transactions.csv` - Validated records
- `data/quarantine/invalid_transactions.csv` - Quarantined records with `failure_reason`
- `data/reports/summary_report.json` - Quality report

## Notes

- `.env` is ignored by Git and must be created locally from `.env.example`
- PostgreSQL data persists across container restarts via the `postgres_data` named volume
- `docker compose down -v` deletes the volume and all local database data (use with caution)
