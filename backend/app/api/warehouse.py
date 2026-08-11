from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Query

from app.database.database import get_db

from app.schemas.warehouse_schema import (
    WarehouseCreate,
    WarehouseUpdate,
    WarehouseResponse,
    AssignManagerRequest
)

from app.services.warehouse_service import WarehouseService

from app.dependencies.auth import require_roles

from app.models.enums import UserRole

router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"]
)
@router.post(
    "",
    response_model=WarehouseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_warehouse(
    warehouse: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.SUPER_ADMIN)
    )
):
    try:
        return WarehouseService.create(
            db,
            warehouse
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.get(
    "",
    response_model=list[WarehouseResponse]
)
def get_all_warehouses(
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):

    if search:
        return WarehouseService.search(
            db,
            search
        )

    return WarehouseService.get_all(db)
@router.get(
    "/{warehouse_id}",
    response_model=WarehouseResponse
)
def get_warehouse(
    warehouse_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):
    try:

        return WarehouseService.get_by_id(
            db,
            warehouse_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
@router.put(
    "/{warehouse_id}",
    response_model=WarehouseResponse
)
def update_warehouse(
    warehouse_id: UUID,
    warehouse: WarehouseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.SUPER_ADMIN)
    )
):
    try:

        return WarehouseService.update(
            db,
            warehouse_id,
            warehouse
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.delete(
    "/{warehouse_id}"
)
def disable_warehouse(
    warehouse_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.SUPER_ADMIN)
    )
):
    try:

        WarehouseService.disable(
            db,
            warehouse_id
        )

        return {
            "message": "Warehouse disabled successfully"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
@router.put(
    "/{warehouse_id}/assign-manager",
    response_model=WarehouseResponse
)
def assign_manager(
    warehouse_id: UUID,
    request: AssignManagerRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.SUPER_ADMIN)
    )
):
    try:

        return WarehouseService.assign_manager(
            db,
            warehouse_id,
            request.manager_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )