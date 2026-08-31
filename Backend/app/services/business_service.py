from uuid import UUID

from fastapi import HTTPException

from app.models.business import Business
from app.repositories.business_repository import BusinessRepository
from app.schemas.business import BusinessCreate, BusinessUpdate


class BusinessService:
    def __init__(self, repo: BusinessRepository):
        self.repo = repo

    def list_businesses(self):
        return self.repo.get_all()

    def get_business(self, business_id: UUID):
        business = self.repo.get(business_id)
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")
        return business

    def create_business(self, data: BusinessCreate):
        business = Business(**data.model_dump())
        return self.repo.create(business)

    def update_business(self, business_id: UUID, data: BusinessUpdate):
        business = self.get_business(business_id)

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(business, key, value)

        return self.repo.update(business)

    def delete_business(self, business_id: UUID):
        business = self.get_business(business_id)
        self.repo.delete(business)