# data-reliability-pipeline

A data reliability pipeline that ingests raw transaction CSV files, transforms and validates the data, quarantines invalid records (instead of deleting them), and generates a data quality report.

## Sections

1. Problem Statement
2. Architecture
3. Folder Structure
4. Validation Rules
5. How To Run
6. Test Instructions
7. Example Outputs
8. Engineering Decisions
9. Future Improvements

---

## 1. Problem Statement

Regional payment agents submit transaction data as CSV files with inconsistent formats, duplicate entries, null fields, and invalid values. This pipeline ensures data quality by:

- Standardizing all incoming data
- Validating every record against business rules
- Quarantining (not deleting) invalid records with a failure reason
- Producing a data quality summary report

## 2. Architecture

The pipeline follows a 6-step flow:

```
Raw Data -> Ingestion -> Transformation -> Validation -> Clean/Quarantine Storage -> Report
```

See [docs/architecture.md](docs/architecture.md) for the full architecture diagram and component breakdown.

## 3. Folder Structure

```
data-reliability-pipeline/
├── data/
│   ├── raw/           # Input CSV files (immutable)
│   ├── clean/         # Validated records
│   ├── quarantine/    # Invalid records with failure reasons
│   └── reports/       # Data quality summary (JSON)
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   └── engineering_decisions.md
├── src/
│   ├── ingest.py      # Load and combine raw CSV files
│   ├── transform.py   # Standardize types, dates, status
│   ├── validation.py  # Validation checks and quarantine logic
│   ├── report.py      # Report generation
│   └── pipeline.py    # Pipeline orchestration
├── tests/
│   ├── test_validation.py
│   ├── test_transform.py
│   └── test_pipeline.py
├── conftest.py
├── requirements.txt
└── README.md
```

## 4. Validation Rules

| Rule              | Check                          | Failure Code          |
|-------------------|--------------------------------|-----------------------|
| Required Columns  | All columns in REQUIRED_COLUMNS present | N/A (raises error) |
| Null Fields       | No nulls in required columns   | `NULL_REQUIRED_FIELD` |
| Duplicates        | transaction_id must be unique  | `DUPLICATE_TRANSACTION` |
| Amount            | amount > 0                     | `INVALID_AMOUNT`      |
| Future Date       | transaction_date <= today      | `INVALID_DATE`        |

Failure reason priority: NULL_REQUIRED_FIELD -> DUPLICATE_TRANSACTION -> INVALID_AMOUNT -> INVALID_DATE.

## 5. How To Run

```bash
pip install -r requirements.txt
python -m src.pipeline
```

The pipeline reads all CSV files from `data/raw/`, writes clean records to `data/clean/clean_transactions.csv`, quarantined records to `data/quarantine/invalid_transactions.csv`, and a summary report to `data/reports/summary_report.json`.

## 6. Test Instructions

```bash
pytest tests/ -v
```

## 7. Example Outputs

### Clean Output (`data/clean/clean_transactions.csv`)

Records that passed all validation checks.

### Quarantine Output (`data/quarantine/invalid_transactions.csv`)

| transaction_id | amount | failure_reason     |
|----------------|--------|--------------------|
| TX003          | -500   | INVALID_AMOUNT     |

### Summary Report (`data/reports/summary_report.json`)

```json
{
  "processed_records": 10,
  "passed_records": 4,
  "failed_records": 6,
  "failure_breakdown": {
    "DUPLICATE_TRANSACTION": 1,
    "INVALID_AMOUNT": 2,
    "INVALID_DATE": 2,
    "NULL_REQUIRED_FIELD": 2
  }
}
```

## 8. Engineering Decisions

See [docs/engineering_decisions.md](docs/engineering_decisions.md) for full ADRs.

Key decisions:
- **Quarantine over deletion** — preserves audit trail (ADR-001)
- **Pandas** for data processing (ADR-002)
- **Priority-based failure tagging** — each record gets one reason (ADR-003)
- **JSON** for summary reports (ADR-004)

## 9. Future Improvements

- Add Great Expectations for richer validation rules
- Add Airflow orchestration for scheduled runs
- Store data in PostgreSQL instead of CSV
- Incremental processing (only new files)
- Dockerization
- CI/CD with GitHub Actions
- Data lineage tracking
