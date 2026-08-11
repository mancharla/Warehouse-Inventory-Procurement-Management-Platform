from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.dependencies.auth import require_roles

from app.models.enums import UserRole

from app.schemas.analytics_schema import (

    DashboardAnalyticsResponse,

    InventoryAnalyticsResponse,

    SupplierAnalyticsResponse,

    WarehouseAnalyticsResponse

)

from app.services.analytics_service import (
    AnalyticsService
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)
@router.get(
    "/dashboard",
    response_model=DashboardAnalyticsResponse
)
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):

    return AnalyticsService.dashboard(db)
@router.get(
    "/inventory",
    response_model=list[InventoryAnalyticsResponse]
)
def inventory_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):

    return AnalyticsService.inventory(db)
@router.get(
    "/suppliers",
    response_model=list[SupplierAnalyticsResponse]
)
def supplier_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.PROCUREMENT_OFFICER
        )
    )
):

    return AnalyticsService.suppliers(db)
@router.get(
    "/warehouses",
    response_model=list[WarehouseAnalyticsResponse]
)
def warehouse_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):

    return AnalyticsService.warehouses(db)