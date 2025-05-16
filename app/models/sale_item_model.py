from sqlalchemy import Column, String, ForeignKey, Numeric
from sqlalchemy.dialects.mysql import CHAR
from ..db.database import Base
from ..mixins.incremental_id_mixin import IncrementalIDMixin
from ..mixins.timestamp_mixin import TimestampMixin

class SaleItem(IncrementalIDMixin, TimestampMixin, Base):
    __tablename__ = "sale_items"

    product_id = Column(CHAR(36), ForeignKey("products.id"), nullable=False, index=True)
    sales_id = Column(CHAR(36), ForeignKey("sales.id"), nullable=False, index=True)
    quantity = Column(Numeric(20), nullable=False)
    per_item_price = Column(Numeric(20), nullable=False)
    total_price = Column(Numeric(20), nullable=False)
