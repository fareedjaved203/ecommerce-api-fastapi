from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from ..utils.response_wrapper import APIResponse
from ..db.database import get_db
from ..schemas.inventory_schema import InventoryCreate, InventoryUpdate, InventoryOut
from ..controllers.inventory_controller import (
    create_inventory,
    update_inventory_by_product,
    get_product_inventory
)

router = APIRouter(prefix="/inventory", tags=["inventory"])

db_dependency = Annotated[Session, Depends(get_db)]

@router.post(
    "/",
    response_model=APIResponse[InventoryOut],
    status_code=201,
    responses={
        404: {"description": "Product not found"},
        400: {"description": "Invalid data"},
        500: {"description": "Database error"}
    }
)
def create_inventory_record(
    inventory: InventoryCreate,
    db: db_dependency
):
    return create_inventory(db, inventory)

@router.put(
    "/product/{product_id}",
    response_model=APIResponse[InventoryOut],
    responses={
        404: {"description": "Product or inventory not found"},
        500: {"description": "Database error"}
    }
)
def update_inventory_by_product_id(
    product_id: str,
    inventory_update: InventoryUpdate,
    db: Session = Depends(get_db)
):
    return update_inventory_by_product(db, product_id, inventory_update)

@router.get(
    "/product/{product_id}",
    response_model=APIResponse[InventoryOut],
    responses={
        404: {"description": "Product or inventory not found"},
        500: {"description": "Database error"}
    }
)
def get_product_inventory_levels(
    product_id: str,
    db: db_dependency
):
    return get_product_inventory(db, product_id)