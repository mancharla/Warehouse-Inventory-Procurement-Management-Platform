import uuid

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import Enum
from sqlalchemy import String

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.enums import PurchaseOrderStatus


class PurchaseOrder(Base):

    __tablename__ = "purchase_orders"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    po_number = Column(
        String(30),
        unique=True,
        nullable=False
    )

    supplier_id = Column(
        UUID(as_uuid=True),
        ForeignKey("suppliers.id"),
        nullable=False
    )

    warehouse_id = Column(
        UUID(as_uuid=True),
        ForeignKey("warehouses.id"),
        nullable=False
    )

    order_date = Column(
        Date,
        nullable=False
    )

    expected_delivery_date = Column(
        Date,
        nullable=False
    )

    status = Column(
        Enum(PurchaseOrderStatus),
        default=PurchaseOrderStatus.PENDING_APPROVAL,
        nullable=False
    )

    total_amount = Column(
        Numeric(12, 2),
        default=0
    )

    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    approved_by = Column(
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

    supplier = relationship("Supplier")
    warehouse = relationship("Warehouse")

    items = relationship(
    "PurchaseOrderItem",
    back_populates="purchase_order",
    cascade="all, delete-orphan"
    )