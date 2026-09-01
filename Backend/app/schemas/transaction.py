from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    business_id: UUID
    inventory_id: UUID
    transaction_type: str = Field(
        pattern="^(ADDED|UPDATED|SOLD|EXPIRED|DONATED)$"
    )
    quantity: Decimal = Field(gt=0)
    reference: str | None = None


class TransactionResponse(BaseModel):
    transaction_id: UUID
    business_id: UUID
    inventory_id: UUID
    transaction_type: str
    quantity: Decimal
    reference: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)