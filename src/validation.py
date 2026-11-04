from src.pipeline.contracts import REQUIRED_COLUMNS, FailureReason
from src.pipeline.validate.transactions import (
    validate_columns,
    validate_nulls,
    validate_duplicates,
    validate_amounts,
    validate_dates,
    run_all_checks,
)

FAILURE_NULL = FailureReason.NULL_REQUIRED_FIELD.value
FAILURE_DUPLICATE = FailureReason.DUPLICATE_TRANSACTION.value
FAILURE_AMOUNT = FailureReason.INVALID_AMOUNT.value
FAILURE_DATE = FailureReason.INVALID_DATE.value
