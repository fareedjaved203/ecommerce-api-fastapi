from enum import Enum
from datetime import date
from typing import Optional
from pydantic import BaseModel
from typing import List
from decimal import Decimal

class TimePeriod(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    annually = "annually"
    custom = "custom"

class RevenueRequest(BaseModel):
    period: TimePeriod
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    platform_id: Optional[int] = None

class RevenueItem(BaseModel):
    date: date
    total_revenue: Decimal
    total_sales: int

    class Config:
        json_encoders = {
            Decimal: lambda v: str(v)
        }

class RevenueResponse(BaseModel):
    items: List[RevenueItem]
    period: TimePeriod
    total_revenue: Decimal
    total_sales: int

    class Config:
        json_encoders = {
            Decimal: lambda v: str(v)
        }