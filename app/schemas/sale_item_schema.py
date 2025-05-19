from decimal import Decimal
from datetime import datetime
from .base_schema import BaseModel
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_validator
class SaleItemIn(BaseModel):
    product_id: str
    quantity: int

class SaleIn(BaseModel):
    platform_id: int
    items: List[SaleItemIn]
    sale_date: Optional[datetime] = None

class SaleItemOut(BaseModel):
    product_id: str
    quantity: int
    per_item_price: Decimal
    total_price: Decimal

class SaleOut(BaseModel):
    id: int
    platform_id: int
    total_amount: Decimal
    sale_date: datetime
    items: List[SaleItemOut] = []
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: str(v)
        }

class RevenueOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, json_encoders={Decimal: lambda v: str(v)})

    type: str
    amount: Decimal
    
class Period(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class CompareRevenueIn(BaseModel):
    periods: List[Period]
    
class CompareRevenueByCategoryIn(BaseModel):
    categories: List[str]
    periods: List[Period]