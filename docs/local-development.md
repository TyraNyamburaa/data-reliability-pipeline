# Local Development Guide

## Prerequisites

- Python 3.10+ (this environment has Python 3.10.12)
- Docker and Docker Compose (installed but requires Docker daemon permissions)

## Quick Start (Local Python)

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the tests:
   ```bash
   python -m pytest tests/ -v
   ```

4. Run the pipeline:
   ```bash
   python -m src.pipeline.main
   ```

## Docker Setup

**Note:** The Docker daemon socket requires appropriate permissions. If you get permission denied:
```bash
sudo usermod -aG docker $USER
# Then log out and back in, or:
sudo docker compose up --build
```

Run with Docker Compose:
```bash
docker compose up --build
docker compose down
```

## Project Structure

```
├── src/pipeline/          # New package structure
│   ├── ingest/            # Data ingestion
│   ├── transform/         # Data transformation
│   ├── validate/          # Data validation & quarantine
│   ├── warehouse/         # Data storage (Postgres)
│   ├── reporting/         # Quality reporting
│   ├── jobs/              # Spark jobs
│   └── main.py            # Entry point
├── tests/                 # Unit tests
├── scripts/               # Utility scripts
├── dags/                  # Airflow DAGs
└── sql/                   # Analytics SQL
```

## Testing

```bash
pytest tests/ -v
```

## Script Usage

- `scripts/generate_sample_data.py` - Generate sample transaction data
- `scripts/kafka_producer.py` - Produce streaming data to Kafka
- `scripts/bootstrap_local_env.sh` - Bootstrap local environment

## Outputs

After running the pipeline:
- `data/processed/clean_transactions.csv` - Validated records
- `data/quarantine/invalid_transactions.csv` - Quarantined records with failure_reason
- `data/reports/summary_report.json` - Quality report

## Docker Startup and Shutdown

### Start the environment
```bash
cp .env.example .env
docker compose up --build
```

### Stop the environment
```bash
docker compose down
```

### Stop and remove volumes (destructive)
```bash
docker compose down -v
```
This deletes the `postgres_data` named volume and all local database data.

### Debugging logs
```bash
docker compose logs postgres
docker compose logs pipeline
```

### Persistence
PostgreSQL data is stored in the `postgres_data` named volume and persists across container restarts.
