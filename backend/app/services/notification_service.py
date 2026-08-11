from app.websocket.connection_manager import manager


class NotificationService:

    # ------------------------------------
    # Inventory Updated
    # ------------------------------------

    @staticmethod
    async def inventory_updated(
        product,
        quantity
    ):

        print(
            "Sending inventory notification:",
            product,
            quantity
        )

        await manager.send_inventory(
            {
                "event": "inventory_updated",
                "product": product,
                "quantity": quantity
            }
        )

    # ------------------------------------
    # Low Stock
    # ------------------------------------

    @staticmethod
    async def low_stock(
        product,
        quantity
    ):

        await manager.send_alert(
            {
                "event": "low_stock",
                "product": product,
                "quantity": quantity
            }
        )

    # ------------------------------------
    # Purchase Order Approved
    # ------------------------------------

    @staticmethod
    async def purchase_order_approved(
        po_number
    ):

        await manager.send_purchase_order(
            {
                "event": "purchase_order_approved",
                "po_number": po_number
            }
        )

    # ------------------------------------
    # Stock Received
    # ------------------------------------

    @staticmethod
    async def stock_received(
        po_number,
        product,
        quantity
    ):

        await manager.send_inventory(
            {
                "event": "stock_received",
                "po_number": po_number,
                "product": product,
                "quantity": quantity
            }
        )

    # ------------------------------------
    # Transfer Approved
    # ------------------------------------

    @staticmethod
    async def transfer_approved(
        transfer_number
    ):

        await manager.send_transfer(
            {
                "event": "transfer_approved",
                "transfer_number": transfer_number
            }
        )

    # ------------------------------------
    # Transfer Completed
    # ------------------------------------

    @staticmethod
    async def transfer_completed(
        transfer_number
    ):

        await manager.send_transfer(
            {
                "event": "transfer_completed",
                "transfer_number": transfer_number
            }
        )

    # ------------------------------------
    # Inventory Audit Due
    # ------------------------------------

    @staticmethod
    async def inventory_audit_due():

        await manager.send_audit(
            {
                "event": "inventory_audit_due",
                "message": (
                    "Inventory audit is due. "
                    "Please review and reconcile inventory."
                )
            }
        )