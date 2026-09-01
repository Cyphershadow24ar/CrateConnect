from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.repositories.inventory_repository import InventoryRepository
from app.schemas.inventory import (
    InventoryCreate,
    InventoryResponse,
    InventoryUpdate,
)
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["Inventory"])


def get_service(db: Session = Depends(get_db)):
    return InventoryService(InventoryRepository(db))


@router.get("", response_model=list[InventoryResponse])
def list_inventory(
    search: Annotated[str | None, Query(description="Search by product name")] = None,
    category_id: Annotated[UUID | None, Query(description="Filter by category")] = None,
    business_id: Annotated[UUID | None, Query(description="Filter by business")] = None,
    expiry_before: Annotated[
        date | None,
        Query(description="Items expiring on or before this date (YYYY-MM-DD)")
    ] = None,
    service: InventoryService = Depends(get_service),
):
    return service.list_inventory(
        search=search,
        category_id=category_id,
        business_id=business_id,
        expiry_before=expiry_before,
    )


@router.get("/{inventory_id}", response_model=InventoryResponse)
def get_inventory(
    inventory_id: UUID,
    service: InventoryService = Depends(get_service),
):
    return service.get_inventory(inventory_id)


@router.post("", response_model=InventoryResponse, status_code=201)
def create_inventory(
    data: InventoryCreate,
    service: InventoryService = Depends(get_service),
):
    return service.create_inventory(data)


@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_id: UUID,
    data: InventoryUpdate,
    service: InventoryService = Depends(get_service),
):
    return service.update_inventory(inventory_id, data)


@router.delete("/{inventory_id}", status_code=204)
def delete_inventory(
    inventory_id: UUID,
    service: InventoryService = Depends(get_service),
):
    service.delete_inventory(inventory_id)