from sqlalchemy import Column, String, ForeignKey, Numeric, JSON, CheckConstraint
from ..db.database import Base
from ..mixins.uuid_mixin import UUIDBinaryMixin
from ..mixins.timestamp_mixin import TimestampMixin

class Product(UUIDBinaryMixin, TimestampMixin, Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_price_non_negative"),
        CheckConstraint("price <= 100000", name="ck_price_reasonable")
    )
        
    name = Column(String(100), unique=True, nullable=False, index=True)
    category_id = Column(String(36), ForeignKey("categories.id"), nullable=False, index=True)
    description = Column(String(300), nullable=True)
    sku = Column(String(20), unique=True, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)    
    images =  Column(JSON, nullable=True)
