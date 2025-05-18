from sqlalchemy import Column, Numeric, ForeignKey, String, Index, CheckConstraint
from ..db.database import Base
from ..mixins.uuid_mixin import UUIDBinaryMixin
from ..mixins.timestamp_mixin import TimestampMixin

class Sale(UUIDBinaryMixin, TimestampMixin, Base):
    __tablename__ = "sales"
    __table_args__ = (
        Index("idx_sales_created_at", "updated_at"),
        CheckConstraint("total_amount >= 0", name="ck_total_amount_non_negative"),
    )

    total_amount = Column(Numeric(10,2), nullable=False)
    platform_id = Column(String(36), ForeignKey("platforms.id"), nullable=False)
