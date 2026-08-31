"""
Seed script — creates demo business and initial food categories.

Run: python -m app.db.seed
"""

import uuid

from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.business import Business
from app.models.category import Category

DEMO_BUSINESS_ID = uuid.UUID(settings.DEMO_BUSINESS_ID)

SEED_CATEGORIES = [
    {"name": "Dairy", "perishability": "HIGH", "storage_type": "COLD"},
    {"name": "Fruits", "perishability": "HIGH", "storage_type": "COLD"},
    {"name": "Bakery", "perishability": "MEDIUM", "storage_type": "DRY"},
    {"name": "Grains", "perishability": "LOW", "storage_type": "DRY"},
    {"name": "Frozen Foods", "perishability": "HIGH", "storage_type": "FROZEN"},
    {"name": "Vegetables", "perishability": "HIGH", "storage_type": "COLD"},
]


def seed_database(db: Session) -> None:
    """Insert demo business and seed categories if they don't exist."""

    # ── Demo Business ─────────────────────────────────
    existing_business = db.get(Business, DEMO_BUSINESS_ID)
    if not existing_business:
        demo_business = Business(
            business_id=DEMO_BUSINESS_ID,
            name="Food Rescue Demo Business",
            email="demo@foodrescue.local",
            phone="+1-555-0100",
            address="123 Demo Street, Food City",
        )
        db.add(demo_business)
        print(f"[OK] Created demo business: {demo_business.name}")
    else:
        print(f"• Demo business already exists: {existing_business.name}")

    # ── Seed Categories ───────────────────────────────
    for cat_data in SEED_CATEGORIES:
        existing = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not existing:
            category = Category(**cat_data)
            db.add(category)
            print(f"[OK] Created category: {cat_data['name']}")
        else:
            print(f"[OK] Category already exists: {cat_data['name']}")

    db.commit()
    print("\nSeed complete.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
