from sqlalchemy import Column, String, ForeignKey, Numeric, Index, CheckConstraint
from sqlalchemy.orm import relationship
from ..db.database import Base
from ..mixins.incremental_id_mixin import IncrementalIDMixin
from ..mixins.timestamp_mixin import TimestampMixin

class Inventory(IncrementalIDMixin, TimestampMixin, Base):
    __tablename__ = "inventories"
    __table_args__ = (
        Index("idx_inventory_updated_at", "updated_at"),
        CheckConstraint("quantity_before >= 0", name="ck_quantity_before_non_negative"),
        CheckConstraint("quantity_after >= 0", name="ck_quantity_after_non_negative"),
        CheckConstraint("threshold >= 0", name="ck_threshold_non_negative"),
        
        CheckConstraint("quantity_before <= 99999", name="ck_quantity_before_max"),
        CheckConstraint("quantity_after <= 99999", name="ck_quantity_after_max"),
        CheckConstraint("threshold <= 999", name="ck_threshold_max"),
    )

    product_id = Column(String(36), ForeignKey("products.id"), nullable=False, index=True)
    product = relationship("Product", back_populates="inventories")
    quantity_changed = Column(Numeric(5, 0), default=0)
    quantity_before = Column(Numeric(5, 0))
    quantity_after = Column(Numeric(5, 0))
    threshold = Column(Numeric(3, 0), default=0)
    reason = Column(String(200), nullable=True)
    
