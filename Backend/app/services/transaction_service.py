from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status

from app.models.inventory_transaction import InventoryTransaction
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreate


class TransactionService:
    def __init__(
        self,
        transaction_repo: TransactionRepository,
        inventory_repo: InventoryRepository,
    ):
        self.transaction_repo = transaction_repo
        self.inventory_repo = inventory_repo

    def list_transactions(self):
        return self.transaction_repo.get_all()

    def get_inventory_history(self, inventory_id: UUID):
        inventory = self.inventory_repo.get(inventory_id)
        if not inventory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory item not found",
            )
        return self.transaction_repo.get_by_inventory(inventory_id)

    def create_transaction(self, data: TransactionCreate):
        inventory = self.inventory_repo.get(data.inventory_id)

        if not inventory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory item not found",
            )

        quantity = Decimal(data.quantity)

        # Stock-changing operations
        if data.transaction_type == "ADDED":
            inventory.quantity += quantity

        elif data.transaction_type in {"SOLD", "DONATED", "EXPIRED"}:
            if inventory.quantity < quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient inventory quantity",
                )
            inventory.quantity -= quantity

        elif data.transaction_type == "UPDATED":
            # Audit-only event (doesn't change quantity)
            pass

        transaction = InventoryTransaction(
            business_id=inventory.business_id,
            inventory_id=inventory.inventory_id,
            transaction_type=data.transaction_type,
            quantity=quantity,
            reference=data.reference,
        )

        self.transaction_repo.create(transaction)
        self.inventory_repo.update(inventory)

        return transaction