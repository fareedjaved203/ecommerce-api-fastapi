from pydantic import BaseModel, condecimal
from typing import Optional, List, Annotated
from .base_schema import BaseSchema

Decimal10_2 = Annotated[condecimal(max_digits=10, decimal_places=2), ...]

class ProductBase(BaseModel):
    name: str
    category_id: str
    description: Optional[str] = None
    sku: str
    price: Decimal10_2
    images: Optional[List[str]] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase, BaseSchema):
    id: str
