from pydantic import BaseModel
from .base_schema import BaseSchema

class CategoryBase(BaseModel):
    name: str
    sku: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryOut(CategoryBase, BaseSchema):
    id: str
