from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
from decimal import Decimal
from typing import List, Dict
from ..schemas.sale_item_schema import CompareRevenueIn, CompareRevenueByCategoryIn
from ..controllers.sales_analysis import (
    get_daily_revenue,
    get_weekly_revenue,
    get_monthly_revenue,
    get_annual_revenue,
    get_custom_revenue,
    get_revenue_for_periods,
    get_revenue_for_categories_periods
)

router = APIRouter(prefix="/revenue", tags=["Revenue"])

@router.get("/daily", response_model=Decimal)
def daily():
    return get_daily_revenue()

@router.get("/weekly", response_model=Decimal)
def weekly():
    return get_weekly_revenue()

@router.get("/monthly", response_model=Decimal)
def monthly():
    return get_monthly_revenue()

@router.get("/annual", response_model=Decimal)
def annual():
    return get_annual_revenue()

@router.get("/custom", response_model=Decimal)
def custom(
    start_date: datetime = Query(..., description="Start datetime in ISO format"),
    end_date: datetime = Query(..., description="End datetime in ISO format"),
):
    try:
        return get_custom_revenue(start_date, end_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/compare", response_model=List[Decimal])
def compare_revenues_by_dates(payload: CompareRevenueIn):
    try:
        periods = [(p.start_date, p.end_date) for p in payload.periods]
        results = get_revenue_for_periods(periods)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/compare-by-category", response_model=List[Dict[str, Decimal]])
def compare_revenue_by_category(payload: CompareRevenueByCategoryIn):
    try:
        periods = [(p.start_date, p.end_date) for p in payload.periods]
        results = get_revenue_for_categories_periods(payload.categories, periods)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))