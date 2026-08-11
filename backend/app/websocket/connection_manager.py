from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):

        self.inventory_connections = []

        self.alert_connections = []

        self.transfer_connections = []

        self.purchase_order_connections = []

        self.audit_connections = []

    # ============================================
    # INVENTORY WEBSOCKET
    # ============================================

    async def connect_inventory(
        self,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.inventory_connections.append(
            websocket
        )

        print(
            "Inventory WebSocket connected. Total:",
            len(self.inventory_connections)
        )

    def disconnect_inventory(
        self,
        websocket: WebSocket
    ):

        if websocket in self.inventory_connections:

            self.inventory_connections.remove(
                websocket
            )

        print(
            "Inventory WebSocket disconnected. Total:",
            len(self.inventory_connections)
        )

    async def send_inventory(
        self,
        message: dict
    ):

        print(
            "Sending inventory notification:",
            message
        )

        print(
            "Sending to inventory connections:",
            len(self.inventory_connections)
        )

        disconnected = []

        for connection in self.inventory_connections:

            try:

                await connection.send_json(
                    message
                )

                print(
                    "Inventory notification sent successfully"
                )

            except Exception as e:

                print(
                    "Inventory WebSocket error:",
                    e
                )

                disconnected.append(
                    connection
                )

        for connection in disconnected:

            self.disconnect_inventory(
                connection
            )

    # ============================================
    # ALERT WEBSOCKET
    # ============================================

    async def connect_alert(
        self,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.alert_connections.append(
            websocket
        )

        print(
            "Alert WebSocket connected. Total:",
            len(self.alert_connections)
        )

    def disconnect_alert(
        self,
        websocket: WebSocket
    ):

        if websocket in self.alert_connections:

            self.alert_connections.remove(
                websocket
            )

        print(
            "Alert WebSocket disconnected. Total:",
            len(self.alert_connections)
        )

    async def send_alert(
        self,
        message: dict
    ):

        print(
            "Sending alert notification:",
            message
        )

        print(
            "Sending to alert connections:",
            len(self.alert_connections)
        )

        disconnected = []

        for connection in self.alert_connections:

            try:

                await connection.send_json(
                    message
                )

                print(
                    "Alert notification sent successfully"
                )

            except Exception as e:

                print(
                    "Alert WebSocket error:",
                    e
                )

                disconnected.append(
                    connection
                )

        for connection in disconnected:

            self.disconnect_alert(
                connection
            )

    # ============================================
    # TRANSFER WEBSOCKET
    # ============================================

    async def connect_transfer(
        self,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.transfer_connections.append(
            websocket
        )

        print(
            "Transfer WebSocket connected. Total:",
            len(self.transfer_connections)
        )

    def disconnect_transfer(
        self,
        websocket: WebSocket
    ):

        if websocket in self.transfer_connections:

            self.transfer_connections.remove(
                websocket
            )

        print(
            "Transfer WebSocket disconnected. Total:",
            len(self.transfer_connections)
        )

    async def send_transfer(
        self,
        message: dict
    ):

        print(
            "Sending transfer notification:",
            message
        )

        print(
            "Sending to transfer connections:",
            len(self.transfer_connections)
        )

        disconnected = []

        for connection in self.transfer_connections:

            try:

                await connection.send_json(
                    message
                )

                print(
                    "Transfer notification sent successfully"
                )

            except Exception as e:

                print(
                    "Transfer WebSocket error:",
                    e
                )

                disconnected.append(
                    connection
                )

        for connection in disconnected:

            self.disconnect_transfer(
                connection
            )

    # ============================================
    # PURCHASE ORDER WEBSOCKET
    # ============================================

    async def connect_purchase_order(
        self,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.purchase_order_connections.append(
            websocket
        )

        print(
            "Purchase Order WebSocket connected. Total:",
            len(self.purchase_order_connections)
        )

    def disconnect_purchase_order(
        self,
        websocket: WebSocket
    ):

        if websocket in self.purchase_order_connections:

            self.purchase_order_connections.remove(
                websocket
            )

        print(
            "Purchase Order WebSocket disconnected. Total:",
            len(self.purchase_order_connections)
        )

    async def send_purchase_order(
        self,
        message: dict
    ):

        print(
            "Sending purchase order notification:",
            message
        )

        print(
            "Sending to purchase order connections:",
            len(self.purchase_order_connections)
        )

        disconnected = []

        for connection in self.purchase_order_connections:

            try:

                await connection.send_json(
                    message
                )

                print(
                    "Purchase order notification sent successfully"
                )

            except Exception as e:

                print(
                    "Purchase Order WebSocket error:",
                    e
                )

                disconnected.append(
                    connection
                )

        for connection in disconnected:

            self.disconnect_purchase_order(
                connection
            )

    # ============================================
    # AUDIT WEBSOCKET
    # ============================================

    async def connect_audit(
        self,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.audit_connections.append(
            websocket
        )

        print(
            "Audit WebSocket connected. Total:",
            len(self.audit_connections)
        )

    def disconnect_audit(
        self,
        websocket: WebSocket
    ):

        if websocket in self.audit_connections:

            self.audit_connections.remove(
                websocket
            )

        print(
            "Audit WebSocket disconnected. Total:",
            len(self.audit_connections)
        )

    async def send_audit(
        self,
        message: dict
    ):

        print(
            "Sending audit notification:",
            message
        )

        print(
            "Sending to audit connections:",
            len(self.audit_connections)
        )

        disconnected = []

        for connection in self.audit_connections:

            try:

                await connection.send_json(
                    message
                )

                print(
                    "Audit notification sent successfully"
                )

            except Exception as e:

                print(
                    "Audit WebSocket error:",
                    e
                )

                disconnected.append(
                    connection
                )

        for connection in disconnected:

            self.disconnect_audit(
                connection
            )


# ============================================
# GLOBAL CONNECTION MANAGER
# ============================================

manager = ConnectionManager()