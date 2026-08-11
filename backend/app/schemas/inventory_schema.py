from uuid import UUID
from typing import Optional
from datetime import datetime, date

from pydantic import BaseModel, Field


# =========================================================
# STOCK IN
# =========================================================

class StockInRequest(BaseModel):

    product_id: UUID

    warehouse_id: UUID

    quantity: int = Field(
        ...,
        gt=0
    )

    batch_number: Optional[str] = None

    expiry_date: Optional[date] = None

    remarks: Optional[str] = None


# =========================================================
# STOCK OUT
# =========================================================

class StockOutRequest(BaseModel):

    product_id: UUID

    warehouse_id: UUID

    quantity: int = Field(
        ...,
        gt=0
    )

    remarks: Optional[str] = None


# =========================================================
# INVENTORY ADJUSTMENT
# =========================================================

class InventoryAdjustRequest(BaseModel):

    product_id: UUID

    warehouse_id: UUID

    available_quantity: int = Field(
        ...,
        ge=0
    )

    reserved_quantity: int = Field(
        ...,
        ge=0
    )

    damaged_quantity: int = Field(
        ...,
        ge=0
    )

    remarks: Optional[str] = None


# =========================================================
# INVENTORY RESPONSE
# =========================================================

class InventoryResponse(BaseModel):

    id: UUID

    product_id: UUID

    warehouse_id: UUID

    available_quantity: int

    reserved_quantity: int

    damaged_quantity: int

    batch_number: Optional[str] = None

    expiry_date: Optional[date] = None

    class Config:
        from_attributes = True


# =========================================================
# INVENTORY TRANSACTION RESPONSE
# =========================================================

class InventoryTransactionResponse(BaseModel):

    id: UUID

    inventory_id: UUID

    product_id: UUID

    warehouse_id: UUID

    transaction_type: str

    quantity: int

    remarks: Optional[str] = None

    created_by: UUID

    created_at: datetime

    class Config:
        from_attributes = True