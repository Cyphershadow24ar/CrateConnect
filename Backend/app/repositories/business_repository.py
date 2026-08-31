from uuid import UUID

from sqlalchemy.orm import Session

from app.models.business import Business


class BusinessRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Business).order_by(Business.name).all()

    def get(self, business_id: UUID):
        return self.db.get(Business, business_id)

    def create(self, business: Business):
        self.db.add(business)
        self.db.commit()
        self.db.refresh(business)
        return business

    def update(self, business: Business):
        self.db.commit()
        self.db.refresh(business)
        return business

    def delete(self, business: Business):
        self.db.delete(business)
        self.db.commit()