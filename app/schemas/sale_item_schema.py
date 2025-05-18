from pydantic import BaseModel, condecimal
from .base_schema import BaseSchema
from typing import Annotated

Decimal11_2 = Annotated[condecimal(max_digits=11, decimal_places=2), ...]
Decimal6_2 = Annotated[condecimal(max_digits=6, decimal_places=2), ...]
Decimal5_0 = Annotated[condecimal(max_digits=5, decimal_places=0), ...]

class SaleItemBase(BaseModel):
    product_id: str
    sales_id: str
    quantity: Decimal5_0
    per_item_price: Decimal6_2
    total_price: Decimal11_2

class SaleItemCreate(SaleItemBase):
    pass

class SaleItemUpdate(SaleItemBase):
    pass

class SaleItemOut(SaleItemBase, BaseSchema):
    id: int
