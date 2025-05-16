import uuid
from typing import Optional, Union
from sqlalchemy import BINARY, Column
from sqlalchemy.ext.hybrid import hybrid_property


class UUIDBinaryMixin:
    _id = Column("id", BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes)

    @hybrid_property
    #false positive error by pylance
    def id(self) -> Optional[str]:
        val = getattr(self, "_id", None)
        if isinstance(val, bytes):
            return str(uuid.UUID(bytes=val))
        return None

    @id.setter  # type: ignore[misc]
    def id(self, value: Union[str, uuid.UUID]) -> None:
        if isinstance(value, uuid.UUID):
            self._id = value.bytes
        elif isinstance(value, str):
            self._id = uuid.UUID(value).bytes
        else:
            raise ValueError("ID must be a UUID or a UUID string")
