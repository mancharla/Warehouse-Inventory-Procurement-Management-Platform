import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Enum

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.enums import TransferStatus


class StockTransfer(Base):

    __tablename__ = "stock_transfers"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    transfer_number = Column(
        String(30),
        unique=True,
        nullable=False
    )

    source_warehouse_id = Column(
        UUID(as_uuid=True),
        ForeignKey("warehouses.id"),
        nullable=False
    )

    destination_warehouse_id = Column(
        UUID(as_uuid=True),
        ForeignKey("warehouses.id"),
        nullable=False
    )

    status = Column(
        Enum(TransferStatus),
        default=TransferStatus.REQUESTED,
        nullable=False
    )

    requested_by = Column(
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

    source_warehouse = relationship(
        "Warehouse",
        foreign_keys=[source_warehouse_id]
    )

    destination_warehouse = relationship(
        "Warehouse",
        foreign_keys=[destination_warehouse_id]
    )

    items = relationship(
        "StockTransferItem",
        back_populates="stock_transfer",
        cascade="all, delete-orphan"
    )