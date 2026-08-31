"""Food category model."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import CheckConstraint, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Category(Base):
    """Food taxonomy with perishability and storage metadata."""

    __tablename__ = "categories"
    __table_args__ = (
        CheckConstraint(
            "perishability IN ('HIGH', 'MEDIUM', 'LOW')",
            name="ck_categories_perishability",
        ),
        CheckConstraint(
            "storage_type IN ('COLD', 'DRY', 'FROZEN')",
            name="ck_categories_storage_type",
        ),
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    perishability: Mapped[str] = mapped_column(String(20), nullable=False)
    storage_type: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Relationships
    inventory_items = relationship("InventoryItem", back_populates="category")
