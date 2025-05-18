from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..models.product_model import Product
from ..schemas.product_schema import ProductCreate, ProductUpdate

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product(product_id: UUID, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def create_product(payload: ProductCreate, db: Session):
    product = Product(**payload.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(product_id: UUID, payload: ProductUpdate, db: Session):
    product = get_product(product_id, db)
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(product_id: UUID, db: Session):
    product = get_product(product_id, db)
    db.delete(product)
    db.commit()
    return {"detail": "Deleted"}
