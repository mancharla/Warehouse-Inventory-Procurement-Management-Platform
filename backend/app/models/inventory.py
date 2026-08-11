import uuid

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Date
from sqlalchemy import String

from app.database.database import Base


class Inventory(Base):

    __tablename__ = "inventory"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )

    warehouse_id = Column(
        UUID(as_uuid=True),
        ForeignKey("warehouses.id", ondelete="CASCADE"),
        nullable=False
    )

    available_quantity = Column(
        Integer,
        default=0,
        nullable=False
    )

    reserved_quantity = Column(
        Integer,
        default=0,
        nullable=False
    )

    damaged_quantity = Column(
        Integer,
        default=0,
        nullable=False
    )
    batch_number = Column(
    String(100),
    nullable=True,
    index=True
    )

    expiry_date = Column(
        Date,
        nullable=True,
        index=True
    )

    last_updated = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    product = relationship("Product")

    warehouse = relationship("Warehouse")