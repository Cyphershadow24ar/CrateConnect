from uuid import UUID
from pydantic import BaseModel, Field
from typing import List


class POSSaleItem(BaseModel):
    barcode: str = Field(..., example="8901234567890")
    quantity: float = Field(..., gt=0, example=2)


class POSSyncRequest(BaseModel):
    business_id: UUID
    pos_name: str = Field(..., example="Demo POS")
    sales: List[POSSaleItem]


class POSUpdatedItem(BaseModel):
    barcode: str
    product_name: str
    sold_quantity: float
    remaining_quantity: float


class POSFailedItem(BaseModel):
    barcode: str
    reason: str


class POSSyncResponse(BaseModel):
    status: str
    pos_name: str
    processed: int
    successful: int
    failed: int
    updated_items: List[POSUpdatedItem]
    failed_items: List[POSFailedItem]