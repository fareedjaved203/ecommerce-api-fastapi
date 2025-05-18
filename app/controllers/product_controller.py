from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..models.product_model import Product
from ..schemas.product_schema import ProductCreate, ProductUpdate
from ..utils.response_wrapper import api_response

def get_all_products(db: Session):
    products = db.query(Product).all()
    return api_response(data=products)

def get_product(product_id: UUID, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return api_response(data=product)

def create_product(payload: ProductCreate, db: Session):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return api_response(data=product, message="Product created successfully")

def update_product(product_id: UUID, payload: ProductUpdate, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return api_response(data=product, message="Product updated successfully")

def delete_product(product_id: UUID, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return api_response(message="Product deleted successfully")
