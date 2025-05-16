from pydantic import BaseModel, condecimal
from typing import Annotated
from .base_schema import BaseSchema

Decimal10_2 = Annotated[condecimal(max_digits=10, decimal_places=2), ...]

class SaleBase(BaseModel):
    total_amount: Decimal10_2
    platform_id: str

class SaleCreate(SaleBase):
    pass

class SaleUpdate(SaleBase):
    pass

class SaleOut(SaleBase, BaseSchema):
    id: str
