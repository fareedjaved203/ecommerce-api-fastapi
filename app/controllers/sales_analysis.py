from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy import func
from ..db.database import SessionLocal
from ..models.sale_model import Sale
from ..models.category_model import Category
from ..models.sale_model import Sale
from ..models.sale_item_model import SaleItem
from ..models.product_model import Product
from typing import List, Tuple
from datetime import datetime
from decimal import Decimal
from typing import List, Tuple, Dict
from sqlalchemy import func
from sqlalchemy.orm import joinedload

def get_revenue(start_date: datetime, end_date: datetime) -> Decimal:
    with SessionLocal() as session:
        total = session.query(func.sum(Sale.total_amount))\
            .filter(Sale.sale_date >= start_date, Sale.sale_date < end_date)\
            .scalar()
        return total or Decimal("0.00")

def get_daily_revenue() -> Decimal:
    today = datetime.utcnow().date()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today + timedelta(days=1), datetime.min.time())
    return get_revenue(start, end)

def get_weekly_revenue() -> Decimal:
    today = datetime.utcnow().date()
    start = today - timedelta(days=today.weekday())  # Monday
    end = start + timedelta(days=7)
    return get_revenue(datetime.combine(start, datetime.min.time()), datetime.combine(end, datetime.min.time()))

def get_monthly_revenue() -> Decimal:
    today = datetime.utcnow().date()
    start = today.replace(day=1)
    if start.month == 12:
        end = start.replace(year=start.year + 1, month=1)
    else:
        end = start.replace(month=start.month + 1)
    return get_revenue(datetime.combine(start, datetime.min.time()), datetime.combine(end, datetime.min.time()))

def get_annual_revenue() -> Decimal:
    today = datetime.utcnow().date()
    start = today.replace(month=1, day=1)
    end = start.replace(year=start.year + 1)
    return get_revenue(datetime.combine(start, datetime.min.time()), datetime.combine(end, datetime.min.time()))

def get_custom_revenue(start_date: datetime, end_date: datetime) -> Decimal:
    if start_date >= end_date:
        raise ValueError("Start date must be before end date.")

    with SessionLocal() as session:
        total = session.query(func.sum(Sale.total_amount))\
            .filter(Sale.sale_date >= start_date, Sale.sale_date < end_date)\
            .scalar()
        return total or Decimal("0.00")

def get_revenue_for_periods(periods: List[Tuple[datetime, datetime]]) -> List[Decimal]:
    results = []
    with SessionLocal() as session:
        for start_date, end_date in periods:
            if start_date >= end_date:
                raise ValueError(f"Start date {start_date} must be before end date {end_date}.")
            total = session.query(func.sum(Sale.total_amount))\
                .filter(Sale.sale_date >= start_date, Sale.sale_date < end_date)\
                .scalar()
            results.append(total or Decimal("0.00"))
    return results

def get_revenue_for_categories_periods(
    categories: List[str], 
    periods: List[Tuple[datetime, datetime]]
) -> List[Dict[str, Decimal]]:
    results = []
    with SessionLocal() as session:
        for start_date, end_date in periods:
            if start_date >= end_date:
                raise ValueError("start_date must be before end_date")

            query = (
                session.query(
                    Category.name.label("category_name"),
                    func.sum(SaleItem.total_price).label("revenue")
                )
                .join(Product, Product.category_id == Category.id)
                .join(SaleItem, SaleItem.product_id == Product.id)
                .join(Sale, Sale.id == SaleItem.sales_id)
                .filter(
                    Sale.sale_date >= start_date,
                    Sale.sale_date < end_date,
                    Category.name.in_(categories)
                )
                .group_by(Category.name)
            )

            period_revenue = {row.category_name: row.revenue or Decimal("0.00") for row in query.all()}
            for cat in categories:
                period_revenue.setdefault(cat, Decimal("0.00"))

            results.append(period_revenue)
    return results

