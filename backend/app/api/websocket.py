from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.websocket.connection_manager import manager
from app.services.notification_service import NotificationService

router = APIRouter(tags=["WebSockets"])
@router.websocket("/ws/inventory")
async def inventory_socket(
    websocket: WebSocket
):

    await manager.connect_inventory(
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect_inventory(
            websocket
        )
@router.websocket("/ws/alerts")
async def alerts_socket(
    websocket: WebSocket
):

    await manager.connect_alert(
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect_alert(
            websocket
        )
@router.websocket("/ws/transfers")
async def transfers_socket(
    websocket: WebSocket
):

    await manager.connect_transfer(
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect_transfer(
            websocket
        )
@router.websocket("/ws/purchase-orders")
async def purchase_order_socket(
    websocket: WebSocket
):

    await manager.connect_purchase_order(
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect_purchase_order(
            websocket
        )
@router.websocket("/ws/audits")
async def audits_socket(
    websocket: WebSocket
):

    await manager.connect_audit(
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect_audit(
            websocket)
        
@router.post("/test-inventory-audit")
async def test_inventory_audit():

    await NotificationService.inventory_audit_due()

    return {
        "message": "Inventory audit notification sent"
    }
@router.post("/test-inventory-notification")
async def test_inventory_notification():

    await NotificationService.inventory_updated(
        "Test Laptop",
        999
    )

    return {
        "message": "Test inventory notification sent"
    }
@router.post("/test-low-stock")
async def test_low_stock():

    await NotificationService.low_stock(
        "Dell Laptop",
        100
    )

    return {
        "message": "Low stock notification sent"
    }
@router.post("/test-purchase-order-approved")
async def test_purchase_order_approved():

    await NotificationService.purchase_order_approved(
        "PO-000001"
    )

    return {
        "message": "Purchase order approved notification sent"
    }
@router.post("/test-transfer-completed")
async def test_transfer_completed():

    await NotificationService.transfer_completed(
        "TR-000001"
    )

    return {
        "message": "Transfer completed notification sent"
    }
@router.post("/test-stock-received")
async def test_stock_received():

    await NotificationService.stock_received(
        "PO-000001",
        "Dell Laptop",
        50
    )

    return {
        "message": "Stock received notification sent"
    }