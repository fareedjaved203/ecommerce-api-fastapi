from sqlalchemy import Column, Integer

class IncrementalIDMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)
