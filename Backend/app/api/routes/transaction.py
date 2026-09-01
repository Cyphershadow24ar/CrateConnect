from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_service(db: Session = Depends(get_db)):
    return TransactionService(
        TransactionRepository(db),
        InventoryRepository(db),
    )


@router.get("", response_model=list[TransactionResponse])
def list_transactions(
    service: TransactionService = Depends(get_service),
):
    return service.list_transactions()


@router.get(
    "/inventory/{inventory_id}",
    response_model=list[TransactionResponse],
)
def inventory_history(
    inventory_id: UUID,
    service: TransactionService = Depends(get_service),
):
    return service.get_inventory_history(inventory_id)


@router.post("", response_model=TransactionResponse, status_code=201)
def create_transaction(
    data: TransactionCreate,
    service: TransactionService = Depends(get_service),
):
    return service.create_transaction(data)