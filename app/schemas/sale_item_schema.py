from pydantic import BaseModel, condecimal
from .base_schema import BaseSchema
from typing import Annotated

Decimal10_2 = Annotated[condecimal(max_digits=10, decimal_places=2), ...]
Decimal10_0 = Annotated[condecimal(max_digits=10, decimal_places=0), ...]

class SaleItemBase(BaseModel):
    product_id: str
    sales_id: str
    quantity: Decimal10_0
    per_item_price: Decimal10_2
    total_price: Decimal10_2

class SaleItemCreate(SaleItemBase):
    pass

class SaleItemUpdate(SaleItemBase):
    pass

class SaleItemOut(SaleItemBase, BaseSchema):
    id: int
