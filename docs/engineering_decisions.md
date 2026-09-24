# Architecture Decision Records (ADR)

## ADR-001: Quarantine Instead of Deletion

**Status:** Accepted

**Context:**
Invalid records must be preserved for audit and debugging. Deleting them loses traceability and makes it impossible to diagnose recurring data issues.

**Decision:**
Quarantined records are written to `data/quarantine/invalid_transactions.csv` with a `failure_reason` column. Records are never deleted from the pipeline.

**Consequences:**
- Data governance compliance is maintained.
- Root cause analysis is possible by inspecting the quarantine file.
- Slight increase in storage usage, which is negligible for batch CSV processing.

---

## ADR-002: Pandas for Data Processing

**Status:** Accepted

**Context:**
The pipeline processes CSV transaction files. We need a library that supports CSV ingestion, type conversion, and filtering.

**Decision:**
Use `pandas` as the primary data processing library. It is lightweight, well-documented, and suitable for batch CSV processing without requiring a database.

**Alternatives Considered:**
- **Polars:** Faster and more memory-efficient, but pandas has broader ecosystem support and is more familiar to reviewers.
- **PySpark:** Overkill for CSV files of this scale.

**Consequences:**
- Simple dependency management.
- Easy to prototype and extend validation logic.

---

## ADR-003: Priority-Based Failure Tagging

**Status:** Accepted

**Context:**
A single record may fail multiple validation checks (e.g., null amount AND future date). The quarantine file needs exactly one `failure_reason` per record for clean grouping in the report.

**Decision:**
Assign failure reasons in priority order:
1. `NULL_REQUIRED_FIELD` - checked first; nulls are the most fundamental issue.
2. `DUPLICATE_TRANSACTION` - duplicate IDs are a data integrity problem.
3. `INVALID_AMOUNT` - non-positive amounts are business rule violations.
4. `INVALID_DATE` - future dates indicate upstream data errors.

A record receives the first matching reason. This ensures each quarantined record has exactly one tag.

**Consequences:**
- The failure_breakdown in the report contains disjoint categories.
- Some records may have additional latent issues not reflected in the primary reason, but the record is still quarantined and visible for manual inspection.

---

## ADR-004: JSON for Summary Report

**Status:** Accepted

**Context:**
The data quality summary report needs to be machine-readable for downstream consumers and human-readable for stakeholder review.

**Decision:**
Use JSON format (`data/reports/summary_report.json`) with 2-space indentation. JSON is universally parseable and requires no additional parsing libraries.

**Consequences:**
- Easy integration with dashboards or monitoring tools.
- Human-readable for quick inspection.
