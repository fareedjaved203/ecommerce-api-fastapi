from pydantic import BaseModel, condecimal, Field
from typing import Optional, Annotated
from decimal import Decimal
from .base_schema import BaseSchema

Numeric5 = Annotated[condecimal(max_digits=5, decimal_places=0), ...]
ThresholdNumeric = Annotated[condecimal(max_digits=3, decimal_places=0), ...]

class InventoryBase(BaseModel):
    product_id: str
    quantity_changed: Decimal = Field(default=Decimal("0"), ge=-99999, le=99999)
    threshold: Optional[Decimal] = Field(None, ge=0, le=999)
    quantity_before: Decimal = Field(default=Decimal("0"), ge=-99999, le=99999)
    quantity_after: Decimal = Field(default=Decimal("0"), ge=-99999, le=99999)
    reason: Optional[str] = Field(None, max_length=200)
    alert: Optional[bool] = None

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(InventoryBase):
    threshold: Optional[Decimal] = Field(None, ge=0, le=999)
    reason: Optional[str] = Field(None, max_length=200)

class InventoryOut(InventoryBase, BaseSchema):
    id: int
