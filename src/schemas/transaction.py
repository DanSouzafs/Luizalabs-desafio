from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, field_validator


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class TransactionIn(BaseModel):
    account_id: int
    type: TransactionType
    amount: Decimal

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v

    class Config:
        use_enum_values = True
