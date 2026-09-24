# Architecture

## Pipeline Overview

```
         ┌─────────────────────────────────────────────────┐
         │          Step 1: Raw Data (Input)               │
         │  data/raw/transactions_2026_01.csv             │
         │  data/raw/transactions_2026_02.csv             │
         └────────────────────────┬────────────────────────┘
                                  │
                                  ▼
         ┌─────────────────────────────────────────────────┐
         │         Step 2: Ingestion  (src/ingest.py)      │
         │  - load_all_data() reads all CSVs from raw/     │
         │  - Concatenates into a single DataFrame         │
         └────────────────────────┬────────────────────────┘
                                  │
                                  ▼
         ┌─────────────────────────────────────────────────┐
         │      Step 3: Transformation (src/transform.py) │
         │  - Lowercase and strip column names             │
         │  - Convert transaction_date → datetime          │
         │  - Convert amount → numeric                     │
         │  - Standardize status via STATUS_MAPPING        │
         └────────────────────────┬────────────────────────┘
                                  │
                                  ▼
         ┌─────────────────────────────────────────────────┐
         │      Step 4: Validation (src/validation.py)   │
         │                                                 │
         │  Columns → Nulls → Duplicates → Amount → Date  │
         │  Each invalid record gets a failure_reason tag  │
         └──────────────┬──────────────────────┬───────────┘
                        │                      │
                        ▼                      ▼
              ┌──────────────┐     ┌──────────────────────┐
              │  Valid       │     │  Invalid (Quarantine)│
              │  records     │     │  records + reason    │
              └──────┬───────┘     └─────────┬────────────┘
                     │                       │
                     ▼                       ▼
         ┌──────────────────┐   ┌──────────────────────────┐
         │ Step 5: Save     │   │ Step 5: Save Quarantine  │
         │ data/clean/      │   │ data/quarantine/          │
         │ clean_transactions│   │ invalid_transactions.csv  │
         │ .csv             │   │                          │
         └────────┬─────────┘   └──────────┬───────────────┘
                  │                        │
                  ▼                        ▼
         ┌──────────────────────────────────────────┐
         │   Step 6: Data Quality Report            │
         │   src/report.py                            │
         │   - Summary: pass/fail counts              │
         │   - failure_breakdown by reason            │
         │   → data/reports/summary_report.json        │
         └──────────────────────────────────────────┘
```

## Components

| Module              | Responsibility                        |
|---------------------|---------------------------------------|
| `src/ingest.py`     | Load and combine raw CSV files        |
| `src/transform.py`  | Standardize types, dates, and status  |
| `src/validation.py` | Run validation checks; quarantine     |
| `src/report.py`     | Build and save data quality report    |
| `src/pipeline.py`   | Orchestrate the full pipeline flow    |
| `tests/`            | Unit and integration tests            |

## Data Zones

```
data/
├── raw/           # Immutable input CSV files
├── clean/         # Validated, production-ready records
├── quarantine/    # Invalid records with failure reasons
└── reports/       # JSON summary report
```

## Design Principles

1. **Data never deletes** - invalid records are quarantined, not dropped.
2. **Single responsibility per module** - each file has a clear purpose.
3. **Explicit failure reasons** - every quarantined record is tagged for traceability.
4. **Human-readable reports** - summary report is JSON for easy consumption.
