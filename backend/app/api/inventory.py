from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    BackgroundTasks,
)
from fastapi import Query

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.inventory_schema import (
    StockInRequest,
    StockOutRequest,
    InventoryAdjustRequest,
    InventoryResponse,
    InventoryTransactionResponse,
)

from app.services.inventory_service import InventoryService

from app.dependencies.auth import require_roles

from app.models.enums import UserRole


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


# =========================================================
# STOCK IN
# =========================================================

@router.post(
    "/stock-in",
    response_model=InventoryResponse,
    status_code=status.HTTP_200_OK
)
def stock_in(
    request: StockInRequest,
    background_tasks: BackgroundTasks,
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

        return InventoryService.stock_in(
            db,
            request,
            current_user,
            background_tasks
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# =========================================================
# GET ALL / SEARCH / FILTER INVENTORY
# =========================================================

@router.get(
    "",
    response_model=list[InventoryResponse]
)
def get_inventory(

    search: Optional[str] = Query(
        None,
        description="Search by product or inventory information"
    ),

    warehouse_id: Optional[str] = Query(
        None,
        description="Filter by warehouse ID"
    ),

    product_id: Optional[str] = Query(
        None,
        description="Filter by product ID"
    ),

    low_stock: bool = Query(
        False,
        description="Show low-stock inventory"
    ),

    out_of_stock: bool = Query(
        False,
        description="Show out-of-stock inventory"
    ),

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

    # -----------------------------------------------------
    # Search
    # -----------------------------------------------------

    if search:

        return InventoryService.search(
            db,
            search
        )

    # -----------------------------------------------------
    # Filters
    # -----------------------------------------------------

    if (
        warehouse_id
        or product_id
        or low_stock
        or out_of_stock
    ):

        return InventoryService.filter_inventory(
            db,
            warehouse_id,
            product_id,
            low_stock,
            out_of_stock
        )

    # -----------------------------------------------------
    # Get All
    # -----------------------------------------------------

    return InventoryService.get_all(
        db
    )


# =========================================================
# INVENTORY HISTORY
# =========================================================

@router.get(
    "/history",
    response_model=list[InventoryTransactionResponse]
)
def inventory_history(

    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):

    return InventoryService.get_history(
        db
    )


# =========================================================
# STOCK OUT
# =========================================================

@router.post(
    "/stock-out",
    response_model=InventoryResponse,
    status_code=status.HTTP_200_OK
)
def stock_out(

    request: StockOutRequest,

    background_tasks: BackgroundTasks,

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

        return InventoryService.stock_out(
            db,
            request,
            current_user,
            background_tasks
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# =========================================================
# ADJUST INVENTORY
# =========================================================

@router.post(
    "/adjust",
    response_model=InventoryResponse,
    status_code=status.HTTP_200_OK
)
def adjust_inventory(

    request: InventoryAdjustRequest,

    background_tasks: BackgroundTasks,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.WAREHOUSE_MANAGER
        )
    )
):

    try:

        return InventoryService.adjust_inventory(
            db,
            request,
            current_user,
            background_tasks
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )