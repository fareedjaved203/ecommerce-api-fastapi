from sqlalchemy import Column, String, ForeignKey, Numeric, CheckConstraint, Boolean
from sqlalchemy.orm import relationship 
from ..db.database import Base
from ..mixins.uuid_mixin import UUIDStringMixin
from ..mixins.timestamp_mixin import TimestampMixin

class Product(UUIDStringMixin, TimestampMixin, Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_price_non_negative"),
        CheckConstraint("price <= 9999.99", name="ck_price_reasonable")
    )
        
    name = Column(String(100), unique=True, nullable=False, index=True)
    category_id = Column(String(36), ForeignKey("categories.id"), nullable=False, index=True)
    description = Column(String(300), nullable=True)
    sku = Column(String(20), unique=True, nullable=False)
    price = Column(Numeric(6, 2), nullable=False)
    published = Column(Boolean, default=False, nullable=False)
    
    category = relationship("Category", back_populates="products")
    inventories = relationship("Inventory", back_populates="product")
    sale_items = relationship("SaleItem", back_populates="product")
