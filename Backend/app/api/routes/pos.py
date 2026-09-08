from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.pos import POSSyncRequest, POSSyncResponse
from app.services.inventory_service import InventoryService
from app.services.pos_service import POSService
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/pos", tags=["POS Integration"])


def get_service(db: Session = Depends(get_db)):
    inventory_service = InventoryService(InventoryRepository(db))
    transaction_service = TransactionService(
        TransactionRepository(db),
        InventoryRepository(db),
    )
    return POSService(inventory_service, transaction_service)


@router.post("/sync", response_model=POSSyncResponse, status_code=200)
def sync_pos_sales(
    data: POSSyncRequest,
    service: POSService = Depends(get_service),
):
    """Sync sales received from an external POS system."""
    return service.sync_sales(data)