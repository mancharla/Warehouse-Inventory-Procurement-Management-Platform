from sqlalchemy.orm import Session
from fastapi import BackgroundTasks

from app.models.inventory import Inventory
from app.models.inventory_transaction import InventoryTransaction
from app.models.product import Product
from app.models.warehouse import Warehouse

from app.repositories.inventory_repository import (
    InventoryRepository,
)

from app.services.inventory_alert_service import (
    InventoryAlertService,
)

from app.services.notification_service import (
    NotificationService,
)


class InventoryService:

    # =========================================================
    # STOCK IN
    # =========================================================

    @staticmethod
    def stock_in(
        db: Session,
        data,
        current_user,
        background_tasks: BackgroundTasks
    ):

        # -----------------------------------------------------
        # Check Product
        # -----------------------------------------------------

        product = (
            db.query(Product)
            .filter(
                Product.id == data.product_id
            )
            .first()
        )

        if product is None:

            raise ValueError(
                "Product not found"
            )

        # -----------------------------------------------------
        # Check Warehouse
        # -----------------------------------------------------

        warehouse = (
            db.query(Warehouse)
            .filter(
                Warehouse.id == data.warehouse_id
            )
            .first()
        )

        if warehouse is None:

            raise ValueError(
                "Warehouse not found"
            )

        # -----------------------------------------------------
        # Get Existing Inventory
        # -----------------------------------------------------

        inventory = (
            InventoryRepository.get_inventory(
                db,
                data.product_id,
                data.warehouse_id
            )
        )

        # =====================================================
        # CREATE INVENTORY
        # =====================================================

        if inventory is None:

            inventory = Inventory(

                product_id=data.product_id,

                warehouse_id=data.warehouse_id,

                available_quantity=data.quantity,

                reserved_quantity=0,

                damaged_quantity=0,

                batch_number=data.batch_number,

                expiry_date=data.expiry_date
            )

            inventory = (
                InventoryRepository.create_inventory(
                    db,
                    inventory
                )
            )

        # =====================================================
        # UPDATE EXISTING INVENTORY
        # =====================================================

        else:

            inventory.available_quantity += data.quantity

            # Update batch number if provided

            if data.batch_number is not None:

                inventory.batch_number = (
                    data.batch_number
                )

            # Update expiry date if provided

            if data.expiry_date is not None:

                inventory.expiry_date = (
                    data.expiry_date
                )

            inventory = (
                InventoryRepository.update_inventory(
                    db,
                    inventory
                )
            )

        # =====================================================
        # GENERATE INVENTORY ALERT
        # =====================================================

        InventoryAlertService.generate(
            db,
            inventory
        )

        # =====================================================
        # WEBSOCKET NOTIFICATION
        # =====================================================

        print(
            "Stock-in completed."
        )

        print(
            "Sending inventory WebSocket notification..."
        )

        print(
            "Product:",
            inventory.product.product_name
        )

        print(
            "Quantity:",
            inventory.available_quantity
        )

        background_tasks.add_task(

            NotificationService.inventory_updated,

            inventory.product.product_name,

            inventory.available_quantity

        )

        print(
            "Inventory WebSocket background task added."
        )

        # =====================================================
        # CREATE INVENTORY TRANSACTION
        # =====================================================

        transaction = InventoryTransaction(

            inventory_id=inventory.id,

            product_id=data.product_id,

            warehouse_id=data.warehouse_id,

            transaction_type="STOCK_IN",

            quantity=data.quantity,

            remarks=data.remarks,

            created_by=current_user.id
        )

        InventoryRepository.add_transaction(
            db,
            transaction
        )

        return inventory

    # =========================================================
    # STOCK OUT
    # =========================================================

    @staticmethod
    def stock_out(
        db: Session,
        data,
        current_user,
        background_tasks: BackgroundTasks
    ):

        # -----------------------------------------------------
        # Get Inventory
        # -----------------------------------------------------

        inventory = (
            InventoryRepository.get_inventory(
                db,
                data.product_id,
                data.warehouse_id
            )
        )

        if inventory is None:

            raise ValueError(
                "Inventory not found"
            )

        # -----------------------------------------------------
        # Check Available Quantity
        # -----------------------------------------------------

        if (
            inventory.available_quantity
            < data.quantity
        ):

            raise ValueError(
                "Insufficient stock"
            )

        # =====================================================
        # DEDUCT STOCK
        # =====================================================

        inventory.available_quantity -= (
            data.quantity
        )

        inventory = (
            InventoryRepository.update_inventory(
                db,
                inventory
            )
        )

        # =====================================================
        # GENERATE ALERT
        # =====================================================

        InventoryAlertService.generate(
            db,
            inventory
        )

        # =====================================================
        # WEBSOCKET NOTIFICATION
        # =====================================================

        print(
            "Stock-out completed."
        )

        print(
            "Sending inventory WebSocket notification..."
        )

        print(
            "Product:",
            inventory.product.product_name
        )

        print(
            "Quantity:",
            inventory.available_quantity
        )

        background_tasks.add_task(

            NotificationService.inventory_updated,

            inventory.product.product_name,

            inventory.available_quantity

        )

        # =====================================================
        # CREATE TRANSACTION
        # =====================================================

        transaction = InventoryTransaction(

            inventory_id=inventory.id,

            product_id=data.product_id,

            warehouse_id=data.warehouse_id,

            transaction_type="STOCK_OUT",

            quantity=data.quantity,

            remarks=data.remarks,

            created_by=current_user.id
        )

        InventoryRepository.add_transaction(
            db,
            transaction
        )

        return inventory

    # =========================================================
    # GET ALL INVENTORY
    # =========================================================

    @staticmethod
    def get_all(
        db: Session
    ):

        return InventoryRepository.get_all(
            db
        )

    # =========================================================
    # GET INVENTORY HISTORY
    # =========================================================

    @staticmethod
    def get_history(
        db: Session
    ):

        return InventoryRepository.get_history(
            db
        )

    # =========================================================
    # ADJUST INVENTORY
    # =========================================================

    @staticmethod
    def adjust_inventory(
        db: Session,
        data,
        current_user,
        background_tasks: BackgroundTasks
    ):

        # -----------------------------------------------------
        # Get Inventory
        # -----------------------------------------------------

        inventory = (
            InventoryRepository.get_inventory(
                db,
                data.product_id,
                data.warehouse_id
            )
        )

        if inventory is None:

            raise ValueError(
                "Inventory not found"
            )

        # =====================================================
        # CALCULATE DIFFERENCE
        # =====================================================

        old_quantity = (
            inventory.available_quantity
        )

        difference = (
            data.available_quantity
            - old_quantity
        )

        # =====================================================
        # UPDATE INVENTORY
        # =====================================================

        inventory.available_quantity = (
            data.available_quantity
        )

        inventory.reserved_quantity = (
            data.reserved_quantity
        )

        inventory.damaged_quantity = (
            data.damaged_quantity
        )

        inventory = (
            InventoryRepository.update_inventory(
                db,
                inventory
            )
        )

        # =====================================================
        # GENERATE ALERT
        # =====================================================

        InventoryAlertService.generate(
            db,
            inventory
        )

        # =====================================================
        # WEBSOCKET NOTIFICATION
        # =====================================================

        print(
            "Inventory adjustment completed."
        )

        print(
            "Sending inventory WebSocket notification..."
        )

        print(
            "Product:",
            inventory.product.product_name
        )

        print(
            "Quantity:",
            inventory.available_quantity
        )

        background_tasks.add_task(

            NotificationService.inventory_updated,

            inventory.product.product_name,

            inventory.available_quantity

        )

        # =====================================================
        # CREATE TRANSACTION
        # =====================================================

        transaction = InventoryTransaction(

            inventory_id=inventory.id,

            product_id=data.product_id,

            warehouse_id=data.warehouse_id,

            transaction_type="ADJUSTMENT",

            quantity=difference,

            remarks=data.remarks,

            created_by=current_user.id
        )

        InventoryRepository.add_transaction(
            db,
            transaction
        )

        return inventory

    # =========================================================
    # SEARCH INVENTORY
    # =========================================================

    @staticmethod
    def search(
        db: Session,
        search: str
    ):

        return InventoryRepository.search(
            db,
            search
        )

    # =========================================================
    # FILTER INVENTORY
    # =========================================================

    @staticmethod
    def filter_inventory(
        db: Session,
        warehouse_id=None,
        product_id=None,
        low_stock=False,
        out_of_stock=False
    ):

        return InventoryRepository.filter_inventory(

            db,

            warehouse_id,

            product_id,

            low_stock,

            out_of_stock

        )