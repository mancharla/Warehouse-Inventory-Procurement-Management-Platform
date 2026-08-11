from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from app.models.enums import AlertType


class InventoryAlertResponse(BaseModel):

    id: UUID

    product_id: UUID

    warehouse_id: UUID

    current_quantity: int

    alert_type: AlertType

    message: str

    is_acknowledged: bool

    created_at: datetime

    class Config:
        from_attributes = True