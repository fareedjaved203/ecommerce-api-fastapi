from sqlalchemy import Column, String
from ..db.database import Base
from ..mixins.uuid_mixin import UUIDBinaryMixin
from ..mixins.timestamp_mixin import TimestampMixin

class Category(UUIDBinaryMixin, TimestampMixin, Base):
    __tablename__ = "categories"

    name = Column(String(100), unique=True, nullable=False, index=True)
    sku = Column(String(20), unique=True, nullable=False)
