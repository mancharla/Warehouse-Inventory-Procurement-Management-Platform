from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Query
from app.database.database import get_db

from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)

from app.services.product_service import ProductService

from app.dependencies.auth import require_roles
from app.models.enums import UserRole

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)
@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):
    try:
        return ProductService.create(db, product)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.get(
    "",
    response_model=list[ProductResponse]
)
def get_products(

    search: Optional[str] = Query(None),

    category: Optional[str] = Query(None),

    brand: Optional[str] = Query(None),

    is_active: Optional[bool] = Query(None),

    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER,
            UserRole.INVENTORY_STAFF,
            UserRole.PROCUREMENT_OFFICER
        )
    )
):

    if search:
        return ProductService.search(
            db,
            search
        )

    if category or brand or is_active is not None:

        return ProductService.filter_products(
            db,
            category,
            brand,
            is_active
        )

    return ProductService.get_all(db)
@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(
        UserRole.SUPER_ADMIN,
        UserRole.WAREHOUSE_MANAGER,
        UserRole.INVENTORY_STAFF,
        UserRole.PROCUREMENT_OFFICER
    ))
):
    try:
        return ProductService.get_by_id(
            db,
            product_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: UUID,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):
    try:
        return ProductService.update(
            db,
            product_id,
            product
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.delete(
    "/{product_id}"
)
def archive_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.SUPER_ADMIN)
    )
):
    try:

        ProductService.archive(
            db,
            product_id
        )

        return {
            "message": "Product archived successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
