from decimal import Decimal

from pydantic import BaseModel, field_validator


class AccountIn(BaseModel):
    user_id: int  # Este campo será ignorado se usar user_id do token
    balance: Decimal

    @field_validator("balance")
    @classmethod
    def validate_balance(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Balance must be positive")
        return v
