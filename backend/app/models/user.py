import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base
from app.models.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    full_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String,
        nullable=False
    )

    role = Column(
        Enum(UserRole),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
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
    warehouses = relationship(
    "Warehouse",
    back_populates="manager")