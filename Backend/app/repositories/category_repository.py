from uuid import UUID

from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Category).order_by(Category.name).all()

    def get(self, category_id: UUID):
        return self.db.get(Category, category_id)

    def create(self, category: Category):
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category: Category):
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Category):
        self.db.delete(category)
        self.db.commit()