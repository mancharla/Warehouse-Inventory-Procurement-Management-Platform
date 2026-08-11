import uuid

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class InventoryBatch(Base):

    __tablename__ = "inventory_batches"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    inventory_id = Column(
        UUID(as_uuid=True),
        ForeignKey("inventory.id", ondelete="CASCADE"),
        nullable=False
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

    batch_number = Column(
        Integer,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    expiry_date = Column(
        Date,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    inventory = relationship("Inventory")

    product = relationship("Product")

    warehouse = relationship("Warehouse")