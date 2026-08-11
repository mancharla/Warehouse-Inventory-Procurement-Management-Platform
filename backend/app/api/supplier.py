from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Query

from app.database.database import get_db

from app.schemas.supplier_schema import (
    SupplierCreate,
    SupplierUpdate,
    SupplierResponse,
)

from app.services.supplier_service import SupplierService

from app.dependencies.auth import require_roles
from app.models.enums import UserRole

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)
@router.post(
    "",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED
)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.PROCUREMENT_OFFICER
        )
    )
):
    try:

        return SupplierService.create(
            db,
            supplier
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.get(
    "",
    response_model=list[SupplierResponse]
)
def get_all_suppliers(
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.PROCUREMENT_OFFICER,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):

    if search:
        return SupplierService.search(
            db,
            search
        )

    return SupplierService.get_all(db)
@router.get(
    "/{supplier_id}",
    response_model=SupplierResponse
)
def get_supplier(
    supplier_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.PROCUREMENT_OFFICER
        )
    )
):
    try:

        return SupplierService.get_by_id(
            db,
            supplier_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
@router.put(
    "/{supplier_id}",
    response_model=SupplierResponse
)
def update_supplier(
    supplier_id: UUID,
    supplier: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.PROCUREMENT_OFFICER
        )
    )
):
    try:

        return SupplierService.update(
            db,
            supplier_id,
            supplier
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.delete(
    "/{supplier_id}"
)
def suspend_supplier(
    supplier_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.SUPER_ADMIN)
    )
):
    try:

        SupplierService.suspend(
            db,
            supplier_id
        )

        return {
            "message": "Supplier suspended successfully"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
