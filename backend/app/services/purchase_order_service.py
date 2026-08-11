from sqlalchemy.orm import Session
import asyncio

from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_item import PurchaseOrderItem
from app.models.inventory import Inventory
from app.models.inventory_transaction import InventoryTransaction
from app.models.supplier import Supplier
from app.models.warehouse import Warehouse
from app.models.product import Product
from app.models.enums import PurchaseOrderStatus

from app.repositories.purchase_order_repository import (
    PurchaseOrderRepository,
)

from app.repositories.inventory_repository import (
    InventoryRepository,
)

from app.services.inventory_alert_service import (
    InventoryAlertService,
)

from app.services.notification_service import (
    NotificationService,
)


class PurchaseOrderService:

    @staticmethod
    def create(
        db: Session,
        data,
        current_user
    ):

        supplier = (
            db.query(Supplier)
            .filter(
                Supplier.id == data.supplier_id
            )
            .first()
        )

        if supplier is None:
            raise ValueError(
                "Supplier not found"
            )

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

        count = db.query(PurchaseOrder).count() + 1

        po_number = f"PO-{count:06d}"

        total_amount = 0

        # ------------------------------------
        # Validate Products and Calculate Total
        # ------------------------------------

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

            total_amount += (
                item.quantity *
                item.unit_price
            )

        # ------------------------------------
        # Create Purchase Order
        # ------------------------------------

        purchase_order = PurchaseOrder(

            po_number=po_number,

            supplier_id=data.supplier_id,

            warehouse_id=data.warehouse_id,

            order_date=data.order_date,

            expected_delivery_date=data.expected_delivery_date,

            total_amount=total_amount,

            status=PurchaseOrderStatus.DRAFT,

            created_by=current_user.id
        )

        purchase_order = (
            PurchaseOrderRepository.create_purchase_order(
                db,
                purchase_order
            )
        )

        # ------------------------------------
        # Create Purchase Order Items
        # ------------------------------------

        for item in data.items:

            po_item = PurchaseOrderItem(

                purchase_order_id=purchase_order.id,

                product_id=item.product_id,

                quantity=item.quantity,

                unit_price=item.unit_price,

                total_price=(
                    item.quantity *
                    item.unit_price
                )
            )

            PurchaseOrderRepository.create_purchase_order_item(
                db,
                po_item
            )

        return PurchaseOrderRepository.get_by_id(
            db,
            purchase_order.id
        )

    @staticmethod
    def get_all(
        db: Session
    ):

        return PurchaseOrderRepository.get_all(db)

    @staticmethod
    def get_by_id(
        db: Session,
        purchase_order_id
    ):

        purchase_order = (
            PurchaseOrderRepository.get_by_id(
                db,
                purchase_order_id
            )
        )

        if purchase_order is None:
            raise ValueError(
                "Purchase Order not found"
            )

        return purchase_order

    # ------------------------------------
    # Submit for Approval
    # ------------------------------------

    @staticmethod
    def submit_for_approval(
        db: Session,
        purchase_order_id
    ):

        purchase_order = (
            PurchaseOrderRepository.get_by_id(
                db,
                purchase_order_id
            )
        )

        if purchase_order is None:
            raise ValueError(
                "Purchase Order not found"
            )

        if (
            purchase_order.status
            != PurchaseOrderStatus.DRAFT
        ):
            raise ValueError(
                "Only draft purchase orders can be submitted for approval"
            )

        purchase_order.status = (
            PurchaseOrderStatus.PENDING_APPROVAL
        )

        return PurchaseOrderRepository.update(
            db,
            purchase_order
        )

    # ------------------------------------
    # Approve Purchase Order
    # ------------------------------------

    @staticmethod
    def approve(
        db: Session,
        purchase_order_id,
        current_user
    ):

        purchase_order = (
            PurchaseOrderRepository.get_by_id(
                db,
                purchase_order_id
            )
        )

        if purchase_order is None:
            raise ValueError(
                "Purchase Order not found"
            )

        if (
            purchase_order.status
            != PurchaseOrderStatus.PENDING_APPROVAL
        ):
            raise ValueError(
                "Only pending purchase orders can be approved"
            )

        # Update Status

        purchase_order.status = (
            PurchaseOrderStatus.APPROVED
        )

        purchase_order.approved_by = (
            current_user.id
        )

        purchase_order = (
            PurchaseOrderRepository.update(
                db,
                purchase_order
            )
        )

        # ------------------------------------
        # Real-Time Notification
        # ------------------------------------

        try:

            asyncio.create_task(

                NotificationService.purchase_order_approved(

                    purchase_order.po_number

                )

            )

        except RuntimeError:
            pass

        return purchase_order

    # ------------------------------------
    # Mark Purchase Order as Ordered
    # ------------------------------------

    @staticmethod
    def mark_as_ordered(
        db: Session,
        purchase_order_id
    ):

        purchase_order = (
            PurchaseOrderRepository.get_by_id(
                db,
                purchase_order_id
            )
        )

        if purchase_order is None:
            raise ValueError(
                "Purchase Order not found"
            )

        if (
            purchase_order.status
            != PurchaseOrderStatus.APPROVED
        ):
            raise ValueError(
                "Only approved purchase orders can be marked as ordered"
            )

        purchase_order.status = (
            PurchaseOrderStatus.ORDERED
        )

        return PurchaseOrderRepository.update(
            db,
            purchase_order
        )

    # ------------------------------------
    # Reject Purchase Order
    # ------------------------------------

    @staticmethod
    def reject(
        db: Session,
        purchase_order_id
    ):

        purchase_order = (
            PurchaseOrderRepository.get_by_id(
                db,
                purchase_order_id
            )
        )

        if purchase_order is None:
            raise ValueError(
                "Purchase Order not found"
            )

        if (
            purchase_order.status
            != PurchaseOrderStatus.PENDING_APPROVAL
        ):
            raise ValueError(
                "Only pending purchase orders can be rejected"
            )

        purchase_order.status = (
            PurchaseOrderStatus.REJECTED
        )

        purchase_order = (
            PurchaseOrderRepository.update(
                db,
                purchase_order
            )
        )

        return purchase_order

    # ------------------------------------
    # Cancel Purchase Order
    # ------------------------------------

    @staticmethod
    def cancel(
        db: Session,
        purchase_order_id
    ):

        purchase_order = (
            PurchaseOrderRepository.get_by_id(
                db,
                purchase_order_id
            )
        )

        if purchase_order is None:
            raise ValueError(
                "Purchase Order not found"
            )

        if (
            purchase_order.status
            == PurchaseOrderStatus.COMPLETED
        ):
            raise ValueError(
                "Completed Purchase Order cannot be cancelled"
            )

        purchase_order.status = (
            PurchaseOrderStatus.CANCELLED
        )

        purchase_order = (
            PurchaseOrderRepository.update(
                db,
                purchase_order
            )
        )

        return purchase_order

    # ------------------------------------
    # Receive Goods
    # ------------------------------------

    @staticmethod
    def receive_goods(
        db: Session,
        purchase_order_id,
        data,
        current_user
    ):

        purchase_order = (
            PurchaseOrderRepository.get_by_id(
                db,
                purchase_order_id
            )
        )

        if purchase_order is None:
            raise ValueError(
                "Purchase Order not found"
            )

        if purchase_order.status not in [

            PurchaseOrderStatus.ORDERED,

            PurchaseOrderStatus.PARTIALLY_RECEIVED

        ]:
            raise ValueError(
                "Only ordered or partially received "
                "purchase orders can receive goods"
            )

        # ------------------------------------
        # Process Each Received Item
        # ------------------------------------

        for receipt_item in data.items:

            po_item = (
                db.query(PurchaseOrderItem)
                .filter(
                    PurchaseOrderItem.id
                    == receipt_item.purchase_order_item_id
                )
                .first()
            )

            if po_item is None:
                raise ValueError(
                    "Purchase Order item not found"
                )

            if (
                po_item.purchase_order_id
                != purchase_order.id
            ):
                raise ValueError(
                    "Purchase Order item does not belong "
                    "to this Purchase Order"
                )

            remaining_quantity = (

                po_item.quantity

                - po_item.received_quantity

            )

            if (
                receipt_item.received_quantity
                > remaining_quantity
            ):
                raise ValueError(
                    f"Cannot receive more than remaining "
                    f"quantity ({remaining_quantity})"
                )

            # ------------------------------------
            # Get Inventory
            # ------------------------------------

            inventory = (
                InventoryRepository.get_inventory(
                    db,
                    po_item.product_id,
                    purchase_order.warehouse_id
                )
            )

            # ------------------------------------
            # Create Inventory
            # ------------------------------------

            if inventory is None:

                inventory = Inventory(

                    product_id=po_item.product_id,

                    warehouse_id=(
                        purchase_order.warehouse_id
                    ),

                    available_quantity=(
                        receipt_item.received_quantity
                    ),

                    reserved_quantity=0,

                    damaged_quantity=0
                )

                inventory = (
                    InventoryRepository.create_inventory(
                        db,
                        inventory
                    )
                )

            # ------------------------------------
            # Update Existing Inventory
            # ------------------------------------

            else:

                inventory.available_quantity += (

                    receipt_item.received_quantity

                )

                inventory = (
                    InventoryRepository.update_inventory(
                        db,
                        inventory
                    )
                )

            # ------------------------------------
            # Update Received Quantity
            # ------------------------------------

            po_item.received_quantity += (

                receipt_item.received_quantity

            )

            db.commit()

            # ------------------------------------
            # Inventory Transaction
            # ------------------------------------

            transaction = InventoryTransaction(

                inventory_id=inventory.id,

                product_id=po_item.product_id,

                warehouse_id=(
                    purchase_order.warehouse_id
                ),

                transaction_type="GOODS_RECEIPT",

                quantity=(
                    receipt_item.received_quantity
                ),

                remarks=(
                    f"Received from "
                    f"{purchase_order.po_number}"
                ),

                created_by=current_user.id
            )

            InventoryRepository.add_transaction(
                db,
                transaction
            )

            # ------------------------------------
            # Generate Inventory Alerts
            # ------------------------------------

            InventoryAlertService.generate(
                db,
                inventory
            )

            # ------------------------------------
            # Real-Time Inventory Updated
            # ------------------------------------

            try:

                asyncio.create_task(

                    NotificationService.inventory_updated(

                        inventory.product.product_name,

                        inventory.available_quantity

                    )

                )

            except RuntimeError:
                pass

            # ------------------------------------
            # Real-Time Stock Received
            # ------------------------------------

            try:

                asyncio.create_task(

                    NotificationService.stock_received(

                        purchase_order.po_number,

                        inventory.product.product_name,

                        receipt_item.received_quantity

                    )

                )

            except RuntimeError:
                pass

        # ------------------------------------
        # Check Receipt Completion
        # ------------------------------------

        db.refresh(purchase_order)

        all_items = (
            PurchaseOrderRepository.get_items(
                db,
                purchase_order.id
            )
        )

        is_completed = all(

            item.received_quantity
            >= item.quantity

            for item in all_items
        )

        # ------------------------------------
        # Update Purchase Order Status
        # ------------------------------------

        if is_completed:

            purchase_order.status = (
                PurchaseOrderStatus.COMPLETED
            )

        else:

            purchase_order.status = (
                PurchaseOrderStatus.PARTIALLY_RECEIVED
            )

        purchase_order = (
            PurchaseOrderRepository.update(
                db,
                purchase_order
            )
        )

        return purchase_order

    # ------------------------------------
    # Search Purchase Orders
    # ------------------------------------

    @staticmethod
    def search(
        db: Session,
        search: str
    ):

        return PurchaseOrderRepository.search(
            db,
            search
        )

    # ------------------------------------
    # Filter Purchase Orders
    # ------------------------------------

    @staticmethod
    def filter_purchase_orders(
        db: Session,
        status=None,
        supplier_id=None,
        warehouse_id=None,
        start_date=None,
        end_date=None
    ):

        return (
            PurchaseOrderRepository.filter_purchase_orders(
                db,
                status,
                supplier_id,
                warehouse_id,
                start_date,
                end_date
            )
        )