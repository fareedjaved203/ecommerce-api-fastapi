import uuid
from sqlalchemy import Column, String
class UUIDStringMixin:    
    id = Column("id", String(36), primary_key=True, default=lambda: str(uuid.uuid4()))