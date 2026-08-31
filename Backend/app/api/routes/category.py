from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


def get_service(db: Session = Depends(get_db)):
    return CategoryService(CategoryRepository(db))


@router.get("", response_model=list[CategoryResponse])
def list_categories(service: CategoryService = Depends(get_service)):
    return service.list_categories()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: UUID, service: CategoryService = Depends(get_service)):
    return service.get_category(category_id)


@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(data: CategoryCreate, service: CategoryService = Depends(get_service)):
    return service.create_category(data)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    service: CategoryService = Depends(get_service),
):
    return service.update_category(category_id, data)


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: UUID, service: CategoryService = Depends(get_service)):
    service.delete_category(category_id)