from enum import Enum


class FailureReason(str, Enum):
    NULL_REQUIRED_FIELD = "NULL_REQUIRED_FIELD"
    DUPLICATE_TRANSACTION = "DUPLICATE_TRANSACTION"
    INVALID_AMOUNT = "INVALID_AMOUNT"
    INVALID_DATE = "INVALID_DATE"


FAILURE_NULL = FailureReason.NULL_REQUIRED_FIELD.value
FAILURE_DUPLICATE = FailureReason.DUPLICATE_TRANSACTION.value
FAILURE_AMOUNT = FailureReason.INVALID_AMOUNT.value
FAILURE_DATE = FailureReason.INVALID_DATE.value


REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "agent_id",
    "transaction_date",
    "amount",
    "status",
]

EXPECTED_DTYPES = {
    "transaction_id": "string",
    "customer_id": "string",
    "agent_id": "string",
    "transaction_date": "datetime",
    "amount": "float",
    "status": "string",
}
