from uuid import UUID

from fastapi import HTTPException

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    def list_categories(self):
        return self.repo.get_all()

    def get_category(self, category_id: UUID):
        category = self.repo.get(category_id)
        if not category:
            raise HTTPException(404, "Category not found")
        return category

    def create_category(self, data: CategoryCreate):
        category = Category(**data.model_dump())
        return self.repo.create(category)

    def update_category(self, category_id: UUID, data: CategoryUpdate):
        category = self.get_category(category_id)

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(category, key, value)

        return self.repo.update(category)

    def delete_category(self, category_id: UUID):
        category = self.get_category(category_id)
        self.repo.delete(category)