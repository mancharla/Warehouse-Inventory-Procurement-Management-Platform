from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Query

from app.database.database import get_db

from app.dependencies.auth import require_roles

from app.models.enums import UserRole

from app.schemas.stock_transfer_schema import (
    StockTransferCreate,
    StockTransferResponse,
)

from app.services.stock_transfer_service import (
    StockTransferService
)

router = APIRouter(
    prefix="/transfers",
    tags=["Stock Transfers"]
)
@router.post(
    "",
    response_model=StockTransferResponse,
    status_code=status.HTTP_201_CREATED
)
def create_transfer(
    request: StockTransferCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.INVENTORY_STAFF
        )
    )
):

    try:

        return StockTransferService.create(
            db,
            request,
            current_user
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.get(
    "",
    response_model=list[StockTransferResponse]
)
def get_transfers(
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER,
            UserRole.INVENTORY_STAFF
        )
    )
):

    if search:
        return StockTransferService.search(
            db,
            search
        )

    return StockTransferService.get_all(db)
@router.get(
    "/{transfer_id}",
    response_model=StockTransferResponse
)
def get_transfer(
    transfer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER,
            UserRole.INVENTORY_STAFF
        )
    )
):

    try:

        return StockTransferService.get_by_id(
            db,
            transfer_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
@router.post(
    "/{transfer_id}/approve",
    response_model=StockTransferResponse
)
def approve_transfer(
    transfer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.WAREHOUSE_MANAGER
        )
    )
):
    try:

        return StockTransferService.approve(
            db,
            transfer_id,
            current_user
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.post(
    "/{transfer_id}/mark-in-transit"
)
def mark_transfer_in_transit(
    transfer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):

    try:
        return StockTransferService.mark_in_transit(
            db,
            transfer_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.post(
    "/{transfer_id}/reject",
    response_model=StockTransferResponse
)
def reject_transfer(
    transfer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.WAREHOUSE_MANAGER
        )
    )
):
    try:

        return StockTransferService.reject(
            db,
            transfer_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.post(
    "/{transfer_id}/receive",
    response_model=StockTransferResponse
)
def receive_transfer(
    transfer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.WAREHOUSE_MANAGER
        )
    )
):
    try:

        return StockTransferService.receive(
            db,
            transfer_id,
            current_user
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )