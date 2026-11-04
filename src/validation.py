from src.pipeline.contracts import FailureReason

FAILURE_NULL = FailureReason.NULL_REQUIRED_FIELD.value
FAILURE_DUPLICATE = FailureReason.DUPLICATE_TRANSACTION.value
FAILURE_AMOUNT = FailureReason.INVALID_AMOUNT.value
FAILURE_DATE = FailureReason.INVALID_DATE.value
