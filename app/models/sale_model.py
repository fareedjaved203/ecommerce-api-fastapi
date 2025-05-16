from sqlalchemy import Column, Numeric, ForeignKey, String, DateTime, func, Index
from ..db.database import Base
from ..mixins.uuid_mixin import UUIDBinaryMixin
from ..mixins.timestamp_mixin import TimestampMixin

class Sale(UUIDBinaryMixin, TimestampMixin, Base):
    __tablename__ = "sales"
    __table_args__ = (
        Index("ix_sales_created_at", "created_at"),
    )

    total_amount = Column(Numeric(10,2), nullable=False)
    platform_id = Column(String(36), ForeignKey("platforms.id"), nullable=False)
