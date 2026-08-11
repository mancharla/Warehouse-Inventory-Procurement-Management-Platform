from uuid import UUID
from decimal import Decimal
from datetime import date
from typing import List

from pydantic import BaseModel, Field

from app.models.enums import PurchaseOrderStatus
class PurchaseOrderItemCreate(BaseModel):

    product_id: UUID

    quantity: int = Field(..., gt=0)

    unit_price: Decimal = Field(..., gt=0)
class PurchaseOrderCreate(BaseModel):

    supplier_id: UUID

    warehouse_id: UUID

    order_date: date

    expected_delivery_date: date

    items: List[PurchaseOrderItemCreate]

class PurchaseOrderUpdate(BaseModel):

    expected_delivery_date: date | None = None

    status: PurchaseOrderStatus | None = None
    
class PurchaseOrderReceiptItem(BaseModel):

    purchase_order_item_id: UUID

    received_quantity: int = Field(..., gt=0)


class PurchaseOrderReceiveRequest(BaseModel):

    items: List[PurchaseOrderReceiptItem]

class PurchaseOrderItemResponse(BaseModel):

    id: UUID

    product_id: UUID

    quantity: int

    received_quantity: int

    unit_price: Decimal

    total_price: Decimal

    class Config:
        from_attributes = True

class PurchaseOrderResponse(BaseModel):

    id: UUID

    po_number: str

    supplier_id: UUID

    warehouse_id: UUID

    order_date: date

    expected_delivery_date: date

    status: PurchaseOrderStatus

    total_amount: Decimal

    created_by: UUID

    approved_by: UUID | None

    items: List[PurchaseOrderItemResponse] = []

    class Config:
        from_attributes = True

