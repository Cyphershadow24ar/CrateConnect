"""Inventory transaction model — immutable audit trail."""

import uuid
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class InventoryTransaction(Base):
    """Immutable record of every stock-changing operation."""

    __tablename__ = "inventory_transactions"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_transaction_quantity_positive"),
        CheckConstraint(
            "transaction_type IN ('ADDED', 'UPDATED', 'SOLD', 'EXPIRED', 'DONATED')",
            name="ck_transaction_type_valid",
        ),
    )

    transaction_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    business_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("businesses.business_id", ondelete="CASCADE"), nullable=False
    )
    inventory_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("inventory_items.inventory_id", ondelete="CASCADE"), nullable=False
    )
    transaction_type: Mapped[str] = mapped_column(String(20), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    reference: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    # Relationships
    business = relationship("Business", back_populates="inventory_transactions")
    inventory_item = relationship("InventoryItem", back_populates="transactions")
