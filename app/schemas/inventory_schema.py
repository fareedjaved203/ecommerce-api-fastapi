from pydantic import BaseModel, condecimal
from typing import Optional, Annotated
from decimal import Decimal
from .base_schema import BaseSchema

Numeric5 = Annotated[condecimal(max_digits=5, decimal_places=0), ...]
ThresholdNumeric = Annotated[condecimal(max_digits=3, decimal_places=0), ...]

class InventoryBase(BaseModel):
    product_id: str
    quantity_changed: Numeric5 = Decimal('0')
    quantity_before: Optional[Numeric5] = None
    quantity_after: Optional[Numeric5] = None
    threshold: ThresholdNumeric = Decimal('5')
    reason: Optional[str] = None

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(InventoryBase):
    pass

class InventoryOut(InventoryBase, BaseSchema):
    id: int
