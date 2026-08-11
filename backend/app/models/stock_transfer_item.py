import uuid

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.database import Base


class StockTransferItem(Base):

    __tablename__ = "stock_transfer_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    transfer_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "stock_transfers.id",
            ondelete="CASCADE"
        ),
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

    stock_transfer = relationship(
        "StockTransfer",
        back_populates="items"
    )

    product = relationship("Product")