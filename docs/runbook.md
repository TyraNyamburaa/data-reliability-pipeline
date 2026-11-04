# Operations Runbook

## Overview
This runbook covers operating, monitoring, and troubleshooting the Transaction Reliability Pipeline.

## Startup Procedures

### Local Python
```bash
pip install -e ".[dev]"
python -m src.pipeline.main
```

### Docker
```bash
cp .env.example .env
docker compose up --build
```

## Shutdown Procedures
```bash
docker compose down
```

### Destructive (removes DB data)
```bash
docker compose down -v
```

## Health Checks
```bash
python -m src.pipeline.health
```

## Monitoring
- Check `data/reports/summary_report.json` for quality metrics
- Check `data/quarantine/invalid_transactions.csv` for failures
- Review structured logs in JSON format

## Troubleshooting

### No data found
Run `python scripts/generate_sample_data.py` to create sample data.

### PostgreSQL connection issues
Pipeline continues with local CSV outputs if PostgreSQL is unavailable.

### Docker permission denied
```bash
sudo usermod -aG docker $USER
```

### Logs
```bash
docker compose logs -f postgres
docker compose logs -f pipeline
```

## On-Call Checklist
- [ ] Pipeline completed successfully
- [ ] Quality report generated
- [ ] Failure rate within threshold
- [ ] No stuck jobs
- [ ] Logs reviewed for errors
