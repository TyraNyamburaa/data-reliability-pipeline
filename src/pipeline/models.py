from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Transaction:
    transaction_id: str
    customer_id: str
    agent_id: str
    transaction_date: datetime
    amount: float
    status: str
    region: Optional[str] = None
    currency: Optional[str] = None
    payment_method: Optional[str] = None


@dataclass
class ValidationResult:
    total_records: int
    valid_records: int
    quarantined_records: int
    failure_counts: dict

    @property
    def failure_rate(self) -> float:
        if self.total_records == 0:
            return 0.0
        return self.quarantined_records / self.total_records

    def to_dict(self) -> dict:
        return {
            "total_records": self.total_records,
            "valid_records": self.valid_records,
            "quarantined_records": self.quarantined_records,
            "failure_rate": round(self.failure_rate, 4),
            "failure_counts": self.failure_counts,
        }
