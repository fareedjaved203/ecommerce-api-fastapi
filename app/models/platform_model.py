from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..db.database import Base
from ..mixins.incremental_id_mixin import IncrementalIDMixin
from ..mixins.timestamp_mixin import TimestampMixin

class Platform(TimestampMixin, IncrementalIDMixin, Base):
    __tablename__ = "platforms"

    name = Column(String(100), unique=True, nullable=False)
    sales = relationship("Sale", back_populates="platform")

