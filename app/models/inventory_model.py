from sqlalchemy import Column, String, ForeignKey, Numeric, Index
from ..db.database import Base
from ..mixins.incremental_id_mixin import IncrementalIDMixin
from ..mixins.timestamp_mixin import TimestampMixin

class Inventory(IncrementalIDMixin, TimestampMixin, Base):
    __tablename__ = "inventories"
    __table_args__ = (
        Index("ix_inventory_created_at", "created_at"),
    )


    product_id = Column(String(36), ForeignKey("products.id"), nullable=False, index=True)
    quantity_changed = Column(Numeric(36), default=0)
    quantity_before = Column(Numeric(36))
    quantity_after = Column(Numeric(36))
    threshold = Column(Numeric(36), default=0)
    reason = Column(String(200), nullable=True)
    
