from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Annotated, List

from ..utils.response_wrapper import APIResponse
from ..db.database import get_db
from ..schemas.product_schema import ProductCreate, ProductUpdate, ProductOut
from ..schemas.base_schema import PaginatedResponse
from ..controllers import product_controller

router = APIRouter(prefix="/products", tags=["Products"])

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/", response_model=APIResponse[PaginatedResponse[ProductOut]])
def list_products(
    page: int = 1,
    limit: int = 100,
    search: str = "",
    category_id: str | None = None,
    db: Session = Depends(get_db)
):
    return product_controller.get_all_products(
        db,
        page=page,
        limit=limit,
        search=search,
        category_id=category_id
    )

@router.get("/{product_id}", response_model=APIResponse[ProductOut])
def retrieve_product(product_id: str, db: db_dependency):
    return product_controller.get_product(product_id, db)

@router.post("/", response_model=APIResponse[ProductOut])
def create_product(payload: ProductCreate, db: db_dependency):
    return product_controller.create_product(payload, db)

@router.put("/{product_id}", response_model=APIResponse[ProductOut])
def update_product(product_id: str, payload: ProductUpdate, db: db_dependency):
    return product_controller.update_product(product_id, payload, db)

@router.delete("/{product_id}")
def delete_product(product_id: str, db: db_dependency):
    return product_controller.delete_product(product_id, db)
