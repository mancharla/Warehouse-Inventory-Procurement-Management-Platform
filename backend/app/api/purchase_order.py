from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Query
from datetime import date


from app.database.database import get_db

from app.schemas.purchase_order_schema import (
    PurchaseOrderCreate,
    PurchaseOrderResponse,
    PurchaseOrderReceiveRequest,
    PurchaseOrderResponse,
)

from app.services.purchase_order_service import PurchaseOrderService

from app.dependencies.auth import require_roles

from app.models.enums import UserRole

router = APIRouter(
    prefix="/purchase-orders",
    tags=["Purchase Orders"]
)
@router.post(
    "",
    response_model=PurchaseOrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_purchase_order(
    request: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.PROCUREMENT_OFFICER,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):
    try:

        return PurchaseOrderService.create(
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
    response_model=list[PurchaseOrderResponse]
)
def get_purchase_orders(

    search: Optional[str] = Query(None),

    status: Optional[str] = Query(None),

    supplier_id: Optional[str] = Query(None),

    warehouse_id: Optional[str] = Query(None),

    start_date: Optional[date] = Query(None),

    end_date: Optional[date] = Query(None),

    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER,
            UserRole.PROCUREMENT_OFFICER
        )
    )
):

    if search:
        return PurchaseOrderService.search(
            db,
            search
        )

    if (
        status
        or supplier_id
        or warehouse_id
        or start_date
        or end_date
    ):
        return PurchaseOrderService.filter_purchase_orders(
            db,
            status,
            supplier_id,
            warehouse_id,
            start_date,
            end_date
        )

    return PurchaseOrderService.get_all(db)
@router.get(
    "/{purchase_order_id}",
    response_model=PurchaseOrderResponse
)
def get_purchase_order(
    purchase_order_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.PROCUREMENT_OFFICER,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):
    try:

        return PurchaseOrderService.get_by_id(
            db,
            purchase_order_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
@router.post(
    "/{purchase_order_id}/approve",
    response_model=PurchaseOrderResponse
)
def approve_purchase_order(
    purchase_order_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.WAREHOUSE_MANAGER
        )
    )
):
    try:

        return PurchaseOrderService.approve(
            db,
            purchase_order_id,
            current_user
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.post(
    "/{purchase_order_id}/reject",
    response_model=PurchaseOrderResponse
)
def reject_purchase_order(
    purchase_order_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.WAREHOUSE_MANAGER
        )
    )
):
    try:

        return PurchaseOrderService.reject(
            db,
            purchase_order_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.delete(
    "/{purchase_order_id}"
)
def cancel_purchase_order(
    purchase_order_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.PROCUREMENT_OFFICER
        )
    )
):
    try:

        PurchaseOrderService.cancel(
            db,
            purchase_order_id
        )

        return {
            "message":"Purchase Order cancelled successfully"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.post(
    "/{purchase_order_id}/receive",
    response_model=PurchaseOrderResponse
)
def receive_goods(
    purchase_order_id: UUID,
    data: PurchaseOrderReceiveRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.WAREHOUSE_MANAGER
        )
    )
):
    try:

        return PurchaseOrderService.receive_goods(
            db,
            purchase_order_id,
            data,
            current_user
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.post(
    "/{purchase_order_id}/submit",
    response_model=PurchaseOrderResponse
)
def submit_purchase_order(
    purchase_order_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.WAREHOUSE_MANAGER,
            UserRole.PROCUREMENT_OFFICER
        )
    )
):

    try:
        return PurchaseOrderService.submit_for_approval(
            db,
            purchase_order_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.post(
    "/{purchase_order_id}/mark-ordered",
    response_model=PurchaseOrderResponse
)
def mark_purchase_order_as_ordered(
    purchase_order_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.WAREHOUSE_MANAGER,
            UserRole.PROCUREMENT_OFFICER
        )
    )
):

    try:
        return PurchaseOrderService.mark_as_ordered(
            db,
            purchase_order_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
