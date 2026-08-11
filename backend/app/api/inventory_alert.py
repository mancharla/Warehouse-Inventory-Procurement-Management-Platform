from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.dependencies.auth import require_roles

from app.models.enums import UserRole

from app.schemas.inventory_alert_schema import (
    InventoryAlertResponse
)

from app.services.inventory_alert_service import (
    InventoryAlertService
)

router = APIRouter(
    prefix="/alerts",
    tags=["Inventory Alerts"]
)
@router.get(
    "",
    response_model=list[InventoryAlertResponse]
)
def get_alerts(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):

    return InventoryAlertService.get_all(db)
@router.put(
    "/{alert_id}/acknowledge",
    response_model=InventoryAlertResponse
)
def acknowledge(
    alert_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):

    try:

        return InventoryAlertService.acknowledge(
            db,
            alert_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )