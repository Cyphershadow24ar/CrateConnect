from app.schemas.pos import (
    POSSyncRequest,
    POSSyncResponse,
    POSUpdatedItem,
    POSFailedItem,
)
from app.schemas.transaction import TransactionCreate
from app.services.inventory_service import InventoryService
from app.services.transaction_service import TransactionService


class POSService:
    def __init__(
        self,
        inventory_service: InventoryService,
        transaction_service: TransactionService,
    ):
        self.inventory_service = inventory_service
        self.transaction_service = transaction_service

    def sync_sales(self, request: POSSyncRequest) -> POSSyncResponse:
        updated_items = []
        failed_items = []

        for sale in request.sales:
            try:
                # Find inventory item using existing barcode lookup
                item = self.inventory_service.get_by_barcode(
                    barcode=sale.barcode,
                    business_id=request.business_id,
                )

                # Reuse existing transaction logic
                transaction = TransactionCreate(
                    business_id=request.business_id,
                    inventory_id=item.inventory_id,
                    transaction_type="SOLD",
                    quantity=sale.quantity,
                    reference=f"POS:{request.pos_name}",
                )

                self.transaction_service.create(transaction)

                # Fetch latest quantity after update
                refreshed = self.inventory_service.get(item.inventory_id)

                updated_items.append(
                    POSUpdatedItem(
                        barcode=item.barcode,
                        product_name=item.product_name,
                        sold_quantity=sale.quantity,
                        remaining_quantity=float(refreshed.quantity),
                    )
                )

            except Exception as e:
                failed_items.append(
                    POSFailedItem(
                        barcode=sale.barcode,
                        reason=str(e),
                    )
                )

        return POSSyncResponse(
            status="success",
            pos_name=request.pos_name,
            processed=len(request.sales),
            successful=len(updated_items),
            failed=len(failed_items),
            updated_items=updated_items,
            failed_items=failed_items,
        )