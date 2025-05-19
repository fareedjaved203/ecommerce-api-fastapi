from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from ..utils.response_wrapper import APIResponse
from ..schemas.base_schema import PaginatedResponse
from ..db.database import get_db
from ..schemas.inventory_schema import InventoryUpdate, InventoryOut
from ..controllers.inventory_controller import (
    update_inventory_by_product,
    get_product_inventory_history
)

router = APIRouter(prefix="/inventory", tags=["inventory"])

db_dependency = Annotated[Session, Depends(get_db)]


@router.put(
    "/product/{product_id}",
    response_model=APIResponse[InventoryOut],
    responses={
        404: {"description": "Product or inventory not found"},
        500: {"description": "Database error"}
    }
)
def create_update_inventory_by_product_id(
    product_id: str,
    inventory_update: InventoryUpdate,
    db: Session = Depends(get_db)
):
    return update_inventory_by_product(db, product_id, inventory_update)

@router.get(
    "/product/{product_id}",
    response_model=APIResponse[PaginatedResponse[InventoryOut]],
    responses={
        404: {"description": "Product or inventory not found"},
        500: {"description": "Database error"}
    }
)
def get_product_inventory_complete_history(
    product_id: str,
    db: db_dependency
):
    return get_product_inventory_history(db, product_id)