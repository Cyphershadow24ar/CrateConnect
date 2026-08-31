from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BusinessBase(BaseModel):
    name: str
    email: str
    phone: str | None = None
    address: str | None = None


class BusinessCreate(BusinessBase):
    pass


class BusinessUpdate(BusinessBase):
    pass


class BusinessResponse(BusinessBase):
    business_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)