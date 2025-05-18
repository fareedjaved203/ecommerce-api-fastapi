from pydantic import BaseModel, condecimal, Field
from typing import Optional, Annotated
from decimal import Decimal
from .base_schema import BaseSchema
from .product_schema import ProductOut

Numeric5 = Annotated[condecimal(max_digits=5, decimal_places=0), ...]
ThresholdNumeric = Annotated[condecimal(max_digits=3, decimal_places=0), ...]

class InventoryBase(BaseModel):
    product_id: str
    quantity_changed: Decimal = Field(default=Decimal("0"), ge=-99999, le=99999)
    threshold: Optional[Decimal] = Field(None, ge=0, le=999)
    quantity_before: Decimal = Field(default=Decimal("0"), ge=-99999, le=99999)
    quantity_after: Decimal = Field(default=Decimal("0"), ge=-99999, le=99999)
    reason: Optional[str] = Field(None, max_length=200)
    alert: Optional[bool] = False
    product: Optional[ProductOut] | None = None 

class InventoryCreate(BaseModel):
    product_id: str
    quantity_changed: Decimal = Field(default=Decimal("100"), ge=0, le=99999)
    threshold: Optional[Decimal] = Field(None, ge=0, le=999)
    reason: str = Field(default="Initial stock adjustment", max_length=200)

class InventoryUpdate(BaseModel):
    quantity_changed: Decimal = Field(default=Decimal("0"), ge=-99999, le=99999)
    threshold: Optional[Decimal] = Field(None, ge=0, le=999)
    reason: Optional[str] = Field(None, max_length=200)
    alert: Optional[bool] = False

class InventoryOut(InventoryBase, BaseSchema):
    id: int
