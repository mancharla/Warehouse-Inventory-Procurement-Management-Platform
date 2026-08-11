from sqlalchemy.orm import Session
import asyncio

from app.models.stock_transfer import StockTransfer
from app.models.stock_transfer_item import StockTransferItem
from app.models.inventory import Inventory
from app.models.inventory_transaction import InventoryTransaction
from app.models.warehouse import Warehouse
from app.models.product import Product
from app.models.enums import TransferStatus

from app.services.inventory_alert_service import InventoryAlertService
from app.services.notification_service import NotificationService

from app.repositories.stock_transfer_repository import (
    StockTransferRepository,
)

from app.repositories.inventory_repository import (
    InventoryRepository,
)


class StockTransferService:

    @staticmethod
    def create(
        db: Session,
        data,
        current_user
    ):

        source = (
            db.query(Warehouse)
            .filter(
                Warehouse.id == data.source_warehouse_id
            )
            .first()
        )

        if source is None:
            raise ValueError(
                "Source warehouse not found"
            )

        destination = (
            db.query(Warehouse)
            .filter(
                Warehouse.id == data.destination_warehouse_id
            )
            .first()
        )

        if destination is None:
            raise ValueError(
                "Destination warehouse not found"
            )

        if source.id == destination.id:
            raise ValueError(
                "Source and Destination warehouse cannot be same"
            )

        count = db.query(StockTransfer).count() + 1

        transfer_number = f"TR-{count:06d}"

        for item in data.items:

            product = (
                db.query(Product)
                .filter(
                    Product.id == item.product_id
                )
                .first()
            )

            if product is None:
                raise ValueError(
                    f"Product {item.product_id} not found"
                )

            inventory = InventoryRepository.get_inventory(
                db,
                item.product_id,
                source.id
            )

            if inventory is None:
                raise ValueError(
                    f"No inventory found for {product.product_name}"
                )

            if inventory.available_quantity < item.quantity:
                raise ValueError(
                    f"Insufficient stock for {product.product_name}"
                )

        transfer = StockTransfer(

            transfer_number=transfer_number,

            source_warehouse_id=source.id,

            destination_warehouse_id=destination.id,

            status=TransferStatus.REQUESTED,

            requested_by=current_user.id
        )

        transfer = (
            StockTransferRepository.create_transfer(
                db,
                transfer
            )
        )

        for item in data.items:

            transfer_item = StockTransferItem(

                transfer_id=transfer.id,

                product_id=item.product_id,

                quantity=item.quantity
            )

            StockTransferRepository.create_transfer_item(
                db,
                transfer_item
            )

        return StockTransferRepository.get_by_id(
            db,
            transfer.id
        )

    @staticmethod
    def get_all(
        db: Session
    ):
        return StockTransferRepository.get_all(db)

    @staticmethod
    def get_by_id(
        db: Session,
        transfer_id
    ):

        transfer = StockTransferRepository.get_by_id(
            db,
            transfer_id
        )

        if transfer is None:
            raise ValueError(
                "Transfer not found"
            )

        return transfer
    @staticmethod
    def approve(
                db: Session,
                transfer_id,
                current_user
            ):
    
                transfer = StockTransferRepository.get_by_id(
                    db,
                    transfer_id
                )
    
                if transfer is None:
                    raise ValueError(
                        "Transfer not found"
                    )
    
                if transfer.status != TransferStatus.REQUESTED:
                    raise ValueError(
                        "Only requested transfers can be approved"
                    )
    
                transfer.status = TransferStatus.APPROVED
    
                transfer.approved_by = current_user.id
    
                transfer = StockTransferRepository.update(
                    db,
                    transfer
                )
    
                try:
                    asyncio.create_task(
                        NotificationService.transfer_approved(
                            transfer.transfer_number
                        )
                    )
                except RuntimeError:
                    # Ignore if no event loop is running.
                    # Later we'll replace this with Redis/Celery.
                    pass
    
                return transfer
    @staticmethod
    def mark_in_transit(
        db: Session,
        transfer_id
    ):

        transfer = StockTransferRepository.get_by_id(
            db,
            transfer_id
        )

        if transfer is None:
            raise ValueError(
                "Transfer not found"
            )

        if transfer.status != TransferStatus.APPROVED:
            raise ValueError(
                "Only approved transfers can be marked as in transit"
            )

        transfer.status = TransferStatus.IN_TRANSIT

        return StockTransferRepository.update(
            db,
            transfer
        )
        
    @staticmethod
    def reject(
        db: Session,
        transfer_id
    ):

        transfer = StockTransferRepository.get_by_id(
            db,
            transfer_id
        )

        if transfer is None:
            raise ValueError(
                "Transfer not found"
            )

        if transfer.status != TransferStatus.REQUESTED:
            raise ValueError(
                "Only requested transfers can be rejected"
            )

        transfer.status = TransferStatus.REJECTED

        return StockTransferRepository.update(
            db,
            transfer
        )
    @staticmethod
    def receive(
        db: Session,
        transfer_id,
        current_user
    ):

        transfer = StockTransferRepository.get_by_id(
            db,
            transfer_id
        )

        if transfer is None:
            raise ValueError(
                "Transfer not found"
            )

        if transfer.status != TransferStatus.IN_TRANSIT:
            raise ValueError(
                "Only in-transit transfers can be received"
            )

        items = StockTransferRepository.get_items(
            db,
            transfer.id
        )

        for item in items:

            # ==========================================
            # SOURCE INVENTORY
            # ==========================================

            source_inventory = (
                InventoryRepository.get_inventory(
                    db,
                    item.product_id,
                    transfer.source_warehouse_id
                )
            )

            if source_inventory is None:
                raise ValueError(
                    "Source inventory not found"
                )

            if (
                source_inventory.available_quantity
                < item.quantity
            ):
                raise ValueError(
                    "Insufficient stock"
                )

            # ==========================================
            # DEDUCT SOURCE INVENTORY
            # ==========================================

            source_inventory.available_quantity -= (
                item.quantity
            )

            source_inventory = (
                InventoryRepository.update_inventory(
                    db,
                    source_inventory
                )
            )

            # Generate source inventory alerts

            InventoryAlertService.generate(
                db,
                source_inventory
            )

            # ==========================================
            # SOURCE INVENTORY WEBSOCKET
            # ==========================================

            try:

                asyncio.create_task(
                    NotificationService.inventory_updated(
                        source_inventory.product.product_name,
                        source_inventory.available_quantity
                    )
                )

            except RuntimeError:
                pass

            # ==========================================
            # DESTINATION INVENTORY
            # ==========================================

            destination_inventory = (
                InventoryRepository.get_inventory(
                    db,
                    item.product_id,
                    transfer.destination_warehouse_id
                )
            )

            # Create destination inventory

            if destination_inventory is None:

                destination_inventory = Inventory(

                    product_id=item.product_id,

                    warehouse_id=(
                        transfer.destination_warehouse_id
                    ),

                    available_quantity=item.quantity,

                    reserved_quantity=0,

                    damaged_quantity=0
                )

                destination_inventory = (
                    InventoryRepository.create_inventory(
                        db,
                        destination_inventory
                    )
                )

            # Update destination inventory

            else:

                destination_inventory.available_quantity += (
                    item.quantity
                )

                destination_inventory = (
                    InventoryRepository.update_inventory(
                        db,
                        destination_inventory
                    )
                )

            # ==========================================
            # DESTINATION ALERT
            # ==========================================

            InventoryAlertService.generate(
                db,
                destination_inventory
            )

            # ==========================================
            # DESTINATION INVENTORY WEBSOCKET
            # ==========================================

            try:

                asyncio.create_task(
                    NotificationService.inventory_updated(
                        destination_inventory.product.product_name,
                        destination_inventory.available_quantity
                    )
                )

            except RuntimeError:
                pass

            # ==========================================
            # TRANSFER OUT TRANSACTION
            # ==========================================

            InventoryRepository.add_transaction(

                db,

                InventoryTransaction(

                    inventory_id=source_inventory.id,

                    product_id=item.product_id,

                    warehouse_id=(
                        transfer.source_warehouse_id
                    ),

                    transaction_type="TRANSFER_OUT",

                    quantity=item.quantity,

                    remarks=(
                        f"Transfer "
                        f"{transfer.transfer_number}"
                    ),

                    created_by=current_user.id
                )
            )

            # ==========================================
            # TRANSFER IN TRANSACTION
            # ==========================================

            InventoryRepository.add_transaction(

                db,

                InventoryTransaction(

                    inventory_id=destination_inventory.id,

                    product_id=item.product_id,

                    warehouse_id=(
                        transfer.destination_warehouse_id
                    ),

                    transaction_type="TRANSFER_IN",

                    quantity=item.quantity,

                    remarks=(
                        f"Transfer "
                        f"{transfer.transfer_number}"
                    ),

                    created_by=current_user.id
                )
            )

        # ==============================================
        # MARK TRANSFER AS RECEIVED
        # ==============================================

        transfer.status = TransferStatus.RECEIVED

        transfer = StockTransferRepository.update(
            db,
            transfer
        )

        # ==============================================
        # TRANSFER COMPLETED WEBSOCKET
        # ==============================================

        try:

            asyncio.create_task(

                NotificationService.transfer_completed(

                    transfer.transfer_number

                )

            )

        except RuntimeError:
            pass

        return transfer
    @staticmethod
    def search(
        db: Session,
        search: str
    ):

        return StockTransferRepository.search(
            db,
            search
        )