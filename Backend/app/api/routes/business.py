from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.business_repository import BusinessRepository
from app.schemas.business import (
    BusinessCreate,
    BusinessResponse,
    BusinessUpdate,
)
from app.services.business_service import BusinessService

router = APIRouter(prefix="/businesses", tags=["Businesses"])


def get_service(db: Session = Depends(get_db)):
    return BusinessService(BusinessRepository(db))


@router.get("", response_model=list[BusinessResponse])
def list_businesses(service: BusinessService = Depends(get_service)):
    return service.list_businesses()


@router.get("/{business_id}", response_model=BusinessResponse)
def get_business(
    business_id: UUID,
    service: BusinessService = Depends(get_service),
):
    return service.get_business(business_id)


@router.post("", response_model=BusinessResponse, status_code=201)
def create_business(
    data: BusinessCreate,
    service: BusinessService = Depends(get_service),
):
    return service.create_business(data)


@router.put("/{business_id}", response_model=BusinessResponse)
def update_business(
    business_id: UUID,
    data: BusinessUpdate,
    service: BusinessService = Depends(get_service),
):
    return service.update_business(business_id, data)


@router.delete("/{business_id}", status_code=204)
def delete_business(
    business_id: UUID,
    service: BusinessService = Depends(get_service),
):
    service.delete_business(business_id)