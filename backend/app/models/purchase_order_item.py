import uuid

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import ForeignKey

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.database import Base


class PurchaseOrderItem(Base):

    __tablename__ = "purchase_order_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    purchase_order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("purchase_orders.id", ondelete="CASCADE"),
        nullable=False
    )

    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )
    received_quantity = Column(
        Integer,
        nullable=False,
        default=0
    )

    unit_price = Column(
        Numeric(10, 2),
        nullable=False
    )

    total_price = Column(
        Numeric(12, 2),
        nullable=False
    )

    purchase_order = relationship(
    "PurchaseOrder",
    back_populates="items"
    )
    product = relationship("Product")