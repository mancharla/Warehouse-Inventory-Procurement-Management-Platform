import uuid

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from sqlalchemy import String

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.enums import AlertType


class InventoryAlert(Base):

    __tablename__ = "inventory_alerts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
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

    current_quantity = Column(
        Integer,
        nullable=False
    )

    alert_type = Column(
        Enum(AlertType),
        nullable=False
    )

    message = Column(
        String(255),
        nullable=False
    )

    is_acknowledged = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    product = relationship("Product")

    warehouse = relationship("Warehouse")