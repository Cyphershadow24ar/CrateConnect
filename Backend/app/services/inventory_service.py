from datetime import date
import io
from uuid import UUID

from fastapi import HTTPException, UploadFile
import pandas as pd

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

    def get_by_barcode(self, barcode: str, business_id: UUID):
        """Look up inventory item by barcode within a business. Raises 404 if not found."""
        inventory = self.repo.get_by_barcode(barcode, business_id)
        if not inventory:
            raise HTTPException(
                status_code=404,
                detail=f"No inventory item found with barcode '{barcode}'",
            )
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

    async def upload_csv(self, file: UploadFile):
        """Validate uploaded CSV before importing."""

        if not file.filename or not file.filename.lower().endswith(".csv"):
            raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

        contents = await file.read()

        try:
            df = pd.read_csv(io.BytesIO(contents))
        except Exception:
            raise HTTPException(
            status_code=400,
            detail="Invalid CSV file."
        )

        required_columns = {
            "business_id",
            "category_id",
            "product_name",
            "barcode",
            "quantity",
            "unit",
            "purchase_date",
            "expiry_date",
        }

        missing = required_columns - set(df.columns)

        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(sorted(missing))}"
            )

        inventory_items = []

        for _, row in df.iterrows():
            inventory_items.append(
                InventoryItem(
                    business_id=row["business_id"],
                    category_id=row["category_id"],
                    product_name=row["product_name"],
                    barcode=str(row["barcode"]),
                    quantity=row["quantity"],
                    unit=row["unit"],
                    purchase_date=pd.to_datetime(row["purchase_date"]).date(),
                    expiry_date=pd.to_datetime(row["expiry_date"]).date(),
                )
            )

        created_items = self.repo.bulk_create(inventory_items)

        return {
            "filename": file.filename,
            "rows_found": len(df),
            "rows_imported": len(created_items),
            "rows_skipped": len(df) - len(created_items),
            "message": "CSV import completed.",
        }