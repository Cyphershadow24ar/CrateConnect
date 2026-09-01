from psycopg import _conninfo_attempts_async
from psycopg import _conninfo_attempts_async
from psycopg import _conninfo_attempts_async
from datetime import date
from uuid import UUID
from fastapi import HTTPException
from app.models.inventory import InventoryItem
from app.repositories.inventory_repository import InventoryRepository
from app.schemas.inventory import InventoryCreate, InventoryUpdate


class InventoryService:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    def list_inventory(
        self,
        search: str | None = None,
        category_id: UUID | None = None,
        business_id: UUID | None = None,
        expiry_before: date | None = None,
    ):
        return self.repo.get_all(
            search=search,
            category_id=category_id,
            business_id=business_id,
            expiry_before=expiry_before,
        )

    def get_inventory(self, inventory_id: UUID):
        inventory = self.repo.get(inventory_id)
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory item not found")
        return inventory

    def create_inventory(self, data: InventoryCreate):
        inventory = InventoryItem(**data.model_dump())
        return self.repo.create(inventory)

    def update_inventory(self, inventory_id: UUID, data: InventoryUpdate):
        inventory = self.get_inventory(inventory_id)

        for key, value in data.model_dump().items():
            setattr(inventory, key, value)

        return self.repo.update(inventory)

    def delete_inventory(self, inventory_id: UUID):
        inventory = self.get_inventory(inventory_id)
        self.repo.delete(inventory)

    def list_expiring(self, threshold_days: int = 3):
        """Return inventory items approaching expiry."""
        items = self.repo.get_expiring(threshold_days)

        result = []
        today = date.today()

        for item in items:
            days_remaining = (item.expiry_date - today).days

            result.append(
                {
                    "inventory_id": str(item.inventory_id),
                    "product_name": item.product_name,
                    "quantity": float(item.quantity),
                    "unit": item.unit,
                    "expiry_date": item.expiry_date,
                    "days_remaining": days_remaining,
                    "status": "EXPIRING_SOON",
                }
            )

        return result


    def list_expired(self):
        """Return already expired inventory items."""
        items = self.repo.get_expired()

        result = []

        for item in items:
            result.append(
                {
                    "inventory_id": str(item.inventory_id),
                    "product_name": item.product_name,
                    "quantity": float(item.quantity),
                    "unit": item.unit,
                    "expiry_date": item.expiry_date,
                    "days_remaining": -1,
                    "status": "EXPIRED",
                }
            )

        return result