from sqlalchemy import Column, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.dialects.mysql import CHAR
from ..db.database import Base
from ..mixins.incremental_id_mixin import IncrementalIDMixin
from ..mixins.timestamp_mixin import TimestampMixin

class SaleItem(IncrementalIDMixin, TimestampMixin, Base):
    __tablename__ = "sale_items"
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_quantity_non_negative"),
        CheckConstraint("per_item_price >= 0", name="ck_per_item_price_non_negative"),
        CheckConstraint("total_price >= 0", name="ck_total_price_non_negative"),
        
        CheckConstraint("quantity <= 99999", name="ck_quantity_max"),
        CheckConstraint("per_item_price <= 9999.99", name="ck_per_item_price_max"),
        CheckConstraint("total_price <= 999989000.01", name="ck_total_price_max"),
    )

    product_id = Column(CHAR(36), ForeignKey("products.id"), nullable=False, index=True)
    sales_id = Column(CHAR(36), ForeignKey("sales.id"), nullable=False, index=True)
    quantity = Column(Numeric(5, 0), nullable=False)
    per_item_price = Column(Numeric(6,2), nullable=False)
    total_price = Column(Numeric(11,2), nullable=False)
