from sqlalchemy import Column, String
from sqlalchemy.orm import relationship 
from ..db.database import Base
from ..mixins.uuid_mixin import UUIDStringMixin
from ..mixins.timestamp_mixin import TimestampMixin

class Category(UUIDStringMixin, TimestampMixin, Base):
    __tablename__ = "categories"

    name = Column(String(100), unique=True, nullable=False, index=True)
    sku = Column(String(20), unique=True, nullable=False)
    
    products = relationship("Product", back_populates="category")

