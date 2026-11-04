# Operations Runbook

## Pipeline Health Check

Verify the pipeline is working:
```bash
python -m pytest tests/ -v
python -m src.pipeline.main
```

## Monitoring

Check the summary report:
```bash
cat data/reports/summary_report.json
```

Check quarantine data for issues:
```bash
cat data/quarantine/invalid_transactions.csv
```

## Common Issues

### No data in raw directory
Generate sample data:
```bash
python scripts/generate_sample_data.py
```

### Docker permission denied
```bash
sudo usermod -aG docker $USER
sudo docker compose up --build
```

### Missing dependencies
Install requirements:
```bash
pip install -r requirements.txt
```

### PostgreSQL connection issues
The pipeline will still write to CSV files and generate a report even if PostgreSQL is unavailable.

## Data Pipeline Steps

1. **Ingest** - Load all CSV files from `data/raw/`
2. **Transform** - Standardize dates, amounts, and statuses
3. **Validate** - Check for nulls, duplicates, invalid amounts, and future dates
4. **Quarantine** - Tag invalid records with failure_reason
5. **Save** - Write clean and quarantine CSVs, optionally to PostgreSQL
6. **Report** - Generate JSON summary with failure breakdown

## Failure Reasons

| Reason | Description |
|-------|-------------|
| NULL_REQUIRED_FIELD | Required field contains null/NaT |
| DUPLICATE_TRANSACTION | Transaction ID is duplicated |
| INVALID_AMOUNT | Amount is zero or negative |
| INVALID_DATE | Transaction date is in the future |

## Emergency Recovery

If the pipeline is corrupted:
1. Clean the processed/quarantine/reports directories
2. Verify the raw data is intact
3. Re-run the pipeline
4. Check the quality report for expected results
