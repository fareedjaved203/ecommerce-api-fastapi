from sqlalchemy import Column, Numeric, ForeignKey, Integer, Index, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..db.database import Base
from ..mixins.incremental_id_mixin import IncrementalIDMixin
from ..mixins.timestamp_mixin import TimestampMixin

class Sale(IncrementalIDMixin, TimestampMixin, Base):
    __tablename__ = "sales"
    __table_args__ = (
        Index("idx_sales_created_at", "updated_at"),
        CheckConstraint("total_amount >= 0", name="ck_total_amount_non_negative"),
        CheckConstraint("total_amount <= 999979000000.00", name="ck_total_amount_max"),
    )

    total_amount = Column(Numeric(14,2), nullable=False)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=False)
    
    sale_date = Column(DateTime, default=datetime.now(timezone.utc))
    
    items = relationship("SaleItem", back_populates="sale")
    platform = relationship("Platform", back_populates="sales")

