from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.warehouse import router as warehouse_router
from app.api.supplier import router as supplier_router
from app.api.product import router as product_router
from app.api.inventory import router as inventory_router
from app.api.purchase_order import router as purchase_order_router
from app.api.stock_transfer import router as stock_transfer_router
from app.api.inventory_alert import router as inventory_alert_router
from app.api.analytics import router as analytics_router
from app.api.websocket import router as websocket_router

app = FastAPI(
    title="Warehouse Inventory & Procurement Management Platform",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(warehouse_router)
app.include_router(supplier_router)
app.include_router(product_router)
app.include_router(inventory_router)
app.include_router(purchase_order_router)
app.include_router(stock_transfer_router)
app.include_router(inventory_alert_router)
app.include_router(analytics_router)
app.include_router(websocket_router)

@app.get("/")
def root():
    return {
        "message": "Warehouse Inventory Management API Running Successfully"
    }