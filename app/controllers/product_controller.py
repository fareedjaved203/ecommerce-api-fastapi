from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

from ..models.product_model import Product
from ..schemas.product_schema import ProductCreate, ProductUpdate, ProductOut
from ..utils.response_wrapper import APIResponse

def get_all_products(db: Session):
    products = db.query(Product).all()
    product_response = [ProductOut.model_validate(p).model_dump() for p in products]
    return APIResponse[list[ProductOut]](
        status=True,
        message="Products retrieved successfully",
        data=product_response,
        error=None
    )


def get_product(product_id: UUID, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
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
    except SQLAlchemyError as e:
        db.rollback()
        print("Database error:", e)
        raise HTTPException(status_code=500, detail="Error creating product")
    except Exception as e:
        db.rollback()
        print("Unexpected error:", e)
        raise HTTPException(status_code=500, detail="Something went wrong")


def update_product(product_id: UUID, payload: ProductUpdate, db: Session):
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


def delete_product(product_id: UUID, db: Session):
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
