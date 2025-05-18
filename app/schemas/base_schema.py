from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List, Generic, TypeVar

T = TypeVar('T')

class BaseSchema(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        
class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    pagination: dict
