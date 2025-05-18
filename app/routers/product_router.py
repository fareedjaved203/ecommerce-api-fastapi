from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from ..db.database import get_db
from ..schemas.product_schema import ProductCreate, ProductUpdate, ProductOut
from ..controllers import product_controller

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return product_controller.get_all_products(db)

@router.get("/{product_id}", response_model=ProductOut)
def retrieve_product(product_id: str, db: Session = Depends(get_db)):
    return product_controller.get_product(UUID(product_id), db)

@router.post("/", response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return product_controller.create_product(payload, db)

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: str, payload: ProductUpdate, db: Session = Depends(get_db)):
    return product_controller.update_product(UUID(product_id), payload, db)

@router.delete("/{product_id}")
def delete_product(product_id: str, db: Session = Depends(get_db)):
    return product_controller.delete_product(UUID(product_id), db)
