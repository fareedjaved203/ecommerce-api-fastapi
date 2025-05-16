from pydantic import BaseModel, condecimal
from typing import Optional, Annotated
from decimal import Decimal
from .base_schema import BaseSchema

Decimal10_2 = Annotated[condecimal(max_digits=10, decimal_places=2), ...]

class InventoryBase(BaseModel):
    product_id: str
    quantity_changed: Decimal10_2 = Decimal('0')
    quantity_before: Optional[Decimal10_2] = None
    quantity_after: Optional[Decimal10_2] = None
    quantity_changed: Decimal10_2 = Decimal('5')
    reason: Optional[str] = None

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(InventoryBase):
    pass

class InventoryOut(InventoryBase, BaseSchema):
    id: int
