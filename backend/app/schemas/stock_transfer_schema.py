from uuid import UUID
from typing import List

from pydantic import BaseModel, Field

from app.models.enums import TransferStatus
class StockTransferItemCreate(BaseModel):

    product_id: UUID

    quantity: int = Field(..., gt=0)
class StockTransferCreate(BaseModel):

    source_warehouse_id: UUID

    destination_warehouse_id: UUID

    items: List[StockTransferItemCreate]
class StockTransferUpdate(BaseModel):

    status: TransferStatus

class StockTransferItemResponse(BaseModel):

    id: UUID

    product_id: UUID

    quantity: int

    class Config:
        from_attributes = True

class StockTransferResponse(BaseModel):

    id: UUID

    transfer_number: str

    source_warehouse_id: UUID

    destination_warehouse_id: UUID

    status: TransferStatus

    requested_by: UUID

    approved_by: UUID | None

    items: List[StockTransferItemResponse] = []

    class Config:
        from_attributes = True

