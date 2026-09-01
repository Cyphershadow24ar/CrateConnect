from uuid import UUID

from sqlalchemy.orm import Session

from app.models.inventory_transaction import InventoryTransaction


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return (
            self.db.query(InventoryTransaction)
            .order_by(InventoryTransaction.created_at.desc())
            .all()
        )

    def get_by_inventory(self, inventory_id: UUID):
        return (
            self.db.query(InventoryTransaction)
            .filter(InventoryTransaction.inventory_id == inventory_id)
            .order_by(InventoryTransaction.created_at.desc())
            .all()
        )

    def create(self, transaction: InventoryTransaction):
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction