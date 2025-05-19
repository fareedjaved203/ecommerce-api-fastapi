from pydantic import BaseModel, condecimal
from typing import Optional, Annotated
from .base_schema import BaseSchema
from .category_schema import CategoryOut

Decimal6_2 = Annotated[condecimal(max_digits=6, decimal_places=2), ...]

class ProductBase(BaseModel):
    name: str
    category_id: str
    description: Optional[str] = None
    sku: str
    price: Decimal6_2
    published: bool = False
class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase, BaseSchema):
    id: str
    category: CategoryOut | None = None