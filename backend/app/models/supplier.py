import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.database import Base


class Supplier(Base):

    __tablename__ = "suppliers"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    supplier_name = Column(
        String(150),
        nullable=False
    )

    contact_person = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    phone = Column(
        String(20),
        nullable=False
    )

    gst_number = Column(
        String(20),
        unique=True,
        nullable=False
    )

    address = Column(
        String,
        nullable=False
    )

    rating = Column(
        Float,
        default=5.0
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