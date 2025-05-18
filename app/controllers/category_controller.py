from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..schemas.category_schema import CategoryCreate, CategoryUpdate
from ..models.category_model import Category
from ..utils.response_wrapper import api_response


def list_categories(db: Session):
    categories = db.query(Category).all()
    return api_response(data=categories)


def retrieve_category(category_id: str, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return api_response(data=category)


def create_category(payload: CategoryCreate, db: Session):
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return api_response(data=category, message="Category created successfully")


def update_category(category_id: str, payload: CategoryUpdate, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return api_response(data=category, message="Category updated successfully")


def delete_category(category_id: str, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return api_response(message="Category deleted successfully")