# Data Dictionary

## Input Data (Raw Zone)

Source: `data/raw/transactions_2026_*.csv`

| Field Name        | Type    | Description                                      | Nullable |
|-------------------|---------|--------------------------------------------------|----------|
| transaction_id    | string  | Unique identifier for each transaction           | No       |
| customer_id       | string  | Identifier for the customer                      | No       |
| agent_id          | string  | Identifier for the processing agent              | No       |
| region            | string  | Geographic region of the transaction             | Yes      |
| transaction_date  | date    | Date the transaction occurred                    | No       |
| amount            | float   | Monetary value of the transaction                | No       |
| currency          | string  | Currency code (e.g., KES)                        | Yes      |
| status            | string  | Transaction status (success, pending, failed)    | No       |
| payment_method    | string  | Payment method used (e.g., Mpesa, mobile_money)  | Yes      |

## Transformed Data

After `transform_data()`:

| Field Name        | Type         | Description                                      | Nullable |
|-------------------|--------------|--------------------------------------------------|----------|
| transaction_id    | string       | Unique identifier for each transaction           | No       |
| customer_id       | string       | Identifier for the customer                      | No       |
| agent_id          | string       | Identifier for the processing agent              | No       |
| region            | string       | Geographic region of the transaction             | Yes      |
| transaction_date  | datetime     | Parsed datetime of the transaction               | No       |
| amount            | float        | Numeric monetary value of the transaction        | No       |
| currency          | string       | Currency code (e.g., KES)                        | Yes      |
| status            | string       | Standardized status: SUCCESS, PENDING, FAILED    | No       |
| payment_method    | string       | Payment method used                              | Yes      |

## Output Data

### Clean Zone - `data/clean/clean_transactions.csv`

Same schema as transformed data. Contains only records that passed all validation checks.

### Quarantine Zone - `data/quarantine/invalid_transactions.csv`

Same schema as transformed data plus an additional field:

| Field Name        | Type   | Description                                      |
|-------------------|--------|--------------------------------------------------|
| failure_reason    | string | Code indicating why the record was quarantined   |

### Quarantine Failure Reasons

| Reason Code            | Description                                           |
|------------------------|-------------------------------------------------------|
| NULL_REQUIRED_FIELD    | One or more required fields contain null/NaT values  |
| DUPLICATE_TRANSACTION  | The transaction_id already exists in the dataset     |
| INVALID_AMOUNT         | The amount is zero or negative                        |
| INVALID_DATE           | The transaction_date is in the future                |

## Report Output - `data/reports/summary_report.json`

| Field Name        | Type   | Description                                      |
|-------------------|--------|--------------------------------------------------|
| processed_records | int    | Total number of records processed                |
| passed_records    | int    | Number of records that passed all checks         |
| failed_records    | int    | Number of records quarantined                    |
| failure_breakdown | object | Count of records per failure reason code         |
