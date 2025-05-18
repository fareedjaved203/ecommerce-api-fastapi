from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from ..schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut
from ..schemas.base_schema import PaginatedResponse
from ..models.category_model import Category
from ..utils.response_wrapper import APIResponse


def list_categories(
    db: Session,
    page: int = 1,
    limit: int = 100,
    search: str = ""
) -> APIResponse[PaginatedResponse[CategoryOut]]:
    try:
        if page < 1:
            page = 1
        if limit < 1:
            limit = 100
            
        skip = (page - 1) * limit
        query = db.query(Category)
        
        if search:
            query = query.filter(
                func.lower(Category.name).contains(func.lower(search)) |
                func.lower(Category.sku).contains(func.lower(search))
            )
        
        categories = query.offset(skip).limit(limit).all()
        total_count = query.with_entities(func.count(Category.id)).scalar()
        page_count = max(1, (total_count + limit - 1) // limit)
        
        response_data = PaginatedResponse[CategoryOut](
            items=[CategoryOut.model_validate(cat) for cat in categories],
            pagination={
                "total_items": total_count,
                "total_pages": page_count,
                "current_page": page,
                "page_size": limit,
                "items_on_page": len(categories),
                "has_next": (page * limit) < total_count,
                "has_previous": page > 1
            }
        )
        
        return APIResponse[PaginatedResponse[CategoryOut]](
            status=True,
            message="Categories retrieved successfully",
            data=response_data,
            error=None
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving categories: {str(e)}"
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