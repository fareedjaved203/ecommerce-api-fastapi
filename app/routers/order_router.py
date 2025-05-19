from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from ..utils.response_wrapper import APIResponse
from ..db.database import get_db
from ..controllers.order_controller import create_order
from ..schemas.sale_item_schema import SaleOut, SaleIn

router = APIRouter(prefix="/orders", tags=["orders"])

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", response_model=APIResponse[SaleOut])
def place_order(
    order_data: SaleIn,
    db: db_dependency
):
    return create_order(db, order_data)