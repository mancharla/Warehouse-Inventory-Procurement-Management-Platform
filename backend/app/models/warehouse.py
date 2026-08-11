import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func

from app.database.database import Base


class Warehouse(Base):

    __tablename__ = "warehouses"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    warehouse_name = Column(
        String(150),
        nullable=False
    )

    code = Column(
        String(30),
        unique=True,
        nullable=False,
        index=True
    )

    address = Column(
        String,
        nullable=False
    )

    capacity = Column(
        Integer,
        nullable=False
    )

    current_utilization = Column(
        Integer,
        default=0
    )

    status = Column(
        Boolean,
        default=True
    )

    manager_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    manager = relationship(
        "User",
        back_populates="warehouses"
    )