from datetime import date, timedelta
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.inventory import InventoryItem

class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        search: str | None = None,
        category_id: UUID | None = None,
        business_id: UUID | None = None,
        expiry_before: date | None = None,
    ):
        query = self.db.query(InventoryItem)

        if search:
            query = query.filter(
            InventoryItem.product_name.ilike(f"%{search}%")
        )

        if category_id:
            query = query.filter(
                InventoryItem.category_id == category_id
            )

        if business_id:
            query = query.filter(
                InventoryItem.business_id == business_id
            )

        if expiry_before:
            query = query.filter(
                InventoryItem.expiry_date <= expiry_before
            )

        return query.all()

    def get(self, inventory_id: UUID):
        return (
            self.db.query(InventoryItem)
            .filter(InventoryItem.inventory_id == inventory_id)
            .first()
        )

    def create(self, inventory: InventoryItem):
        self.db.add(inventory)
        self.db.commit()
        self.db.refresh(inventory)
        return inventory

    def update(self, inventory: InventoryItem):
        self.db.commit()
        self.db.refresh(inventory)
        return inventory

    def delete(self, inventory: InventoryItem):
        self.db.delete(inventory)
        self.db.commit()
    
    def get_expiring(self, threshold_days: int = 3):
        """Return items expiring within threshold days."""
        today = date.today()
        limit = today + timedelta(days=threshold_days)

        return (
            self.db.query(InventoryItem)
            .filter(
                InventoryItem.expiry_date >= today,
                InventoryItem.expiry_date <= limit,
            )
            .order_by(InventoryItem.expiry_date.asc())
        .all()
        )


    def get_expired(self):
        """Return already expired items."""
        today = date.today()

        return (
            self.db.query(InventoryItem)
            .filter(InventoryItem.expiry_date < today)
            .order_by(InventoryItem.expiry_date.asc())
            .all()
        )