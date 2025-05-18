from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut
from ..models.category_model import Category


def list_categories(db: Session):
    return db.query(Category).all()


def retrieve_category(category_id: str, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def create_category(payload: CategoryCreate, db: Session):
    category = Category(**payload.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(category_id: str, payload: CategoryUpdate, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


def delete_category(category_id: str, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"detail": "Category deleted"}