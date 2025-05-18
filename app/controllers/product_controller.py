from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import func

from ..models.product_model import Product
from ..schemas.product_schema import ProductCreate, ProductUpdate, ProductOut
from ..schemas.category_schema import CategoryOut
from ..schemas.base_schema import PaginatedResponse
from ..utils.response_wrapper import APIResponse

def get_all_products(
    db: Session,
    page: int = 1,
    limit: int = 100,
    search: str = "",
    category_id: str | None = None
) -> APIResponse[PaginatedResponse[ProductOut]]:
    try:
        if page < 1:
            page = 1
        if limit < 1:
            limit = 100
            
        skip = (page - 1) * limit
        
        query = db.query(Product).options(joinedload(Product.category))
        
        if search:
            query = query.filter(func.lower(Product.name).contains(func.lower(search)))
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        count_query = query.with_entities(func.count(Product.id))
        total_count = count_query.scalar()
        
        products = query.offset(skip).limit(limit).all()
        
        product_data = []
        for product in products:
            product_dict = ProductOut.model_validate(product).model_dump()
            
            if product.category:
                product_dict['category'] = CategoryOut.model_validate({
                    'id': product.category.id,
                    'name': product.category.name,
                    'sku': product.category.sku
                }).model_dump()
            
            product_data.append(product_dict)
        
        page_count = max(1, (total_count + limit - 1) // limit)
        
        response_data = PaginatedResponse[ProductOut](
            items=product_data,
            pagination={
                "total_items": total_count,
                "total_pages": page_count,
                "current_page": page,
                "page_size": limit,
                "items_on_page": len(products),
                "has_next": (page * limit) < total_count,
                "has_previous": page > 1
            }
        )
        
        return APIResponse[PaginatedResponse[ProductOut]](
            status=True,
            message="Products retrieved successfully",
            data=response_data,
            error=None
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving products: {str(e)}"
        )


def get_product(product_id: str, db: Session):
    product = db.query(Product).filter(Product.id == product_id.strip()).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_response = ProductOut.model_validate(product)
    return APIResponse[ProductOut](
        status=True,
        message="Product retrieved successfully",
        data=product_response,
        error=None
    )


def create_product(payload: ProductCreate, db: Session):
    try:
        existing_product = db.query(Product).filter(
            (func.lower(Product.name) == func.lower(payload.name)) |
            (func.lower(Product.sku) == func.lower(payload.sku))
        ).first()
                
        if existing_product:
            raise HTTPException(
                status_code=409,
                detail="Product with this name or sku already exists"
            )
        product = Product(**payload.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        
        product_response = ProductOut.model_validate(product)
        return APIResponse[ProductOut](
            status=True,
            message="Product created successfully",
            data=product_response,
            error=None
        )
        
    except HTTPException:
        raise
        
    except IntegrityError as e:
        db.rollback()
        if "Duplicate entry" in str(e.orig):
            raise HTTPException(
                status_code=409,
                detail="Product with this name already exists"
            )
        raise HTTPException(
            status_code=400,
            detail="Database integrity error"
        )
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error: " + str(e)
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def update_product(product_id: str, payload: ProductUpdate, db: Session):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        db.commit()
        db.refresh(product)
        product_response = ProductOut.model_validate(product)
        return APIResponse[ProductOut](
            status=True,
            message="Product updated successfully",
            data=product_response,
            error=None
        )
    except SQLAlchemyError as e:
        db.rollback()
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Error updating product")
    except Exception as e:
        db.rollback()
        print("Unexpected error:", e)
        raise HTTPException(status_code=500, detail="Something went wrong")


def delete_product(product_id: str, db: Session):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        db.delete(product)
        db.commit()
        return APIResponse[None](
            status=True,
            message="Product deleted successfully",
            data=None,
            error=None
        )
    except SQLAlchemyError as e:
        db.rollback()
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Error deleting product")
    except Exception as e:
        db.rollback()
        print("Unexpected error:", e)
        raise HTTPException(status_code=500, detail="Something went wrong")
