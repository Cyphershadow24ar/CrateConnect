from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class InventoryBase(BaseModel):
    business_id: UUID
    category_id: UUID
    product_name: str
    barcode: str | None = None
    quantity: Decimal
    unit: str
    purchase_date: date | None = None
    expiry_date: date


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(InventoryBase):
    pass


class InventoryResponse(InventoryBase):
    inventory_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)