from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str
    perishability: str
    storage_type: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    category_id: UUID

    model_config = ConfigDict(from_attributes=True)