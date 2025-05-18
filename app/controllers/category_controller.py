from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from uuid import UUID

from ..schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut
from ..models.category_model import Category
from ..utils.response_wrapper import APIResponse


def list_categories(db: Session):
    categories = db.query(Category).all()
    category_response = [CategoryOut.model_validate(cat).model_dump() for cat in categories]

    return APIResponse[List[CategoryOut]](
        status=True,
        message="Categories retrieved successfully",
        data=category_response,
        error=None
    )


def retrieve_category(category_id: str, db: Session):    
    category = db.query(Category).filter(Category.id == category_id.strip()).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category_response = CategoryOut.model_validate(category)
    return APIResponse[CategoryOut](
        status=True,
        message="Category retrieved successfully",
        data=category_response,
        error=None
    )


def create_category(payload: CategoryCreate, db: Session):
    try:
        print("Received payload:", payload.model_dump())
        category = Category(**payload.model_dump())
        db.add(category)
        db.commit()
        db.refresh(category)
        category_response = CategoryOut.model_validate(category)
        return APIResponse[CategoryOut](
            status=True,
            message="Category created successfully",
            data=category_response,
            error=None
        )
    except SQLAlchemyError as e:
        db.rollback()
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Error creating category")
    except Exception as e:
        db.rollback()
        print("Something Went Wrong:", e)
        raise HTTPException(status_code=500, detail="Something Went Wrong")


def update_category(category_id: str, payload: CategoryUpdate, db: Session):
    try:        
        category = db.query(Category).filter(Category.id == category_id.strip()).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(category, key, value)

        db.commit()
        db.refresh(category)
        category_response = CategoryOut.model_validate(category)
        return APIResponse[CategoryOut](
            status=True,
            message="Category updated successfully",
            data=category_response,
            error=None
        )
    except SQLAlchemyError as e:
        db.rollback()
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Error updating category")
    except Exception as e:
        db.rollback()
        print("Something Went Wrong:", e)
        raise HTTPException(status_code=500, detail="Something Went Wrong")


def delete_category(category_id: str, db: Session):
    try:
        category = db.query(Category).filter(Category.id == category_id.strip()).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        db.delete(category)
        db.commit()
        return APIResponse[None](
            status=True,
            message="Category deleted successfully",
            data=None,
            error=None
        )
    except SQLAlchemyError as e:
        db.rollback()
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Error deleting category")
    except Exception as e:
        db.rollback()
        print("Something Went Wrong:", e)
        raise HTTPException(status_code=500, detail="Something Went Wrong")