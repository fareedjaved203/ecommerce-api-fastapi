from pydantic import BaseModel
from .base_schema import BaseSchema

class PlatformBase(BaseModel):
    name: str

class PlatformCreate(PlatformBase):
    pass

class PlatformUpdate(PlatformBase):
    pass

class PlatformOut(PlatformBase, BaseSchema):
    id: int
