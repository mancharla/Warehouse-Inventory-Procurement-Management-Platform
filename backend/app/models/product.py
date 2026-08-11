import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.database import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    sku = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    product_name = Column(
        String(150),
        nullable=False
    )

    category = Column(
        String(100),
        nullable=False
    )

    brand = Column(
        String(100),
        nullable=False
    )

    unit = Column(
        String(30),
        nullable=False
    )

    cost_price = Column(
        Numeric(10, 2),
        nullable=False
    )

    selling_price = Column(
        Numeric(10, 2),
        nullable=False
    )

    reorder_level = Column(
        Integer,
        nullable=False
    )

    barcode = Column(
        String(100),
        unique=True,
        nullable=True
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