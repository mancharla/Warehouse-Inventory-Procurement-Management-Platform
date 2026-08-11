import uuid

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base


class InventoryTransaction(Base):

    __tablename__ = "inventory_transactions"

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
        ForeignKey("products.id"),
        nullable=False
    )

    warehouse_id = Column(
        UUID(as_uuid=True),
        ForeignKey("warehouses.id"),
        nullable=False
    )

    transaction_type = Column(
        String(50),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    remarks = Column(
        String(255),
        nullable=True
    )

    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    inventory = relationship("Inventory")