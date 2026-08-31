"""Inventory item model."""

import uuid
from datetime import UTC, date, datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class InventoryItem(Base):
    """Tenant-owned food inventory item."""

    __tablename__ = "inventory_items"
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_inventory_quantity_non_negative"),
        UniqueConstraint(
            "business_id",
            "barcode",
            name="uq_inventory_business_barcode",
        ),
        Index("ix_inventory_business_id", "business_id"),
        Index("ix_inventory_business_expiry", "business_id", "expiry_date"),
        Index("ix_inventory_business_category", "business_id", "category_id"),
    )

    inventory_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    business_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("businesses.business_id", ondelete="CASCADE"), nullable=False
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("categories.category_id"), nullable=False
    )
    product_name: Mapped[str] = mapped_column(String(150), nullable=False)
    barcode: Mapped[str | None] = mapped_column(String(100), nullable=True)
    quantity: Mapped[Decimal] = mapped_column(
        Numeric(12, 3), nullable=False
    )
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    purchase_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Relationships
    business = relationship("Business", back_populates="inventory_items")
    category = relationship("Category", back_populates="inventory_items")
    transactions = relationship(
        "InventoryTransaction", back_populates="inventory_item", cascade="all, delete-orphan"
    )
