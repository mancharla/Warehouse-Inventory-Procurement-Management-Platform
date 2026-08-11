from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import extract

from datetime import datetime

from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.inventory import Inventory
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_item import PurchaseOrderItem
from app.models.inventory_transaction import InventoryTransaction
from app.models.supplier import Supplier
from app.models.enums import PurchaseOrderStatus

class AnalyticsRepository:
    @staticmethod
    def total_products(db: Session):

        return db.query(Product).count()
    @staticmethod
    def total_warehouses(db: Session):

        return db.query(Warehouse).count()
    @staticmethod
    def inventory_value(db: Session):

        value = (

            db.query(

                func.sum(

                    Inventory.available_quantity *

                    Product.cost_price

                )

            )

            .join(Product)

            .scalar()

        )

        return value or 0
    @staticmethod
    def low_stock_items(db: Session):

        return (

            db.query(Inventory)

            .join(Product)

            .filter(

                Inventory.available_quantity <= Product.reorder_level,

                Inventory.available_quantity > 0

            )

            .count()

        )
    @staticmethod
    def out_of_stock_items(db: Session):

        return (

            db.query(Inventory)

            .filter(

                Inventory.available_quantity == 0

            )

            .count()

        )
    @staticmethod
    def purchase_orders_this_month(db: Session):

        month = datetime.now().month

        year = datetime.now().year

        return (

            db.query(PurchaseOrder)

            .filter(

                extract("month", PurchaseOrder.order_date) == month,

                extract("year", PurchaseOrder.order_date) == year

            )

            .count()

        )
    @staticmethod
    def inventory_turnover(db: Session):

        total_moved = (
            db.query(
                func.sum(InventoryTransaction.quantity)
            )
            .scalar()
        ) or 0

        total_inventory = (
            db.query(
                func.sum(Inventory.available_quantity)
            )
            .scalar()
        ) or 0

        if total_inventory == 0:
            return 0

        return round(total_moved / total_inventory, 2)
    @staticmethod
    def supplier_performance(db: Session):

        total = db.query(PurchaseOrder).count()

        if total == 0:
            return 0

        completed = (
            db.query(PurchaseOrder)
            .filter(
                PurchaseOrder.status ==
                PurchaseOrderStatus.COMPLETED
            )
            .count()
        )

        return round((completed / total) * 100, 2)
    @staticmethod
    def warehouse_utilization(db: Session):

        warehouses = db.query(Warehouse).all()

        if not warehouses:
            return 0

        total = 0

        for warehouse in warehouses:

            if warehouse.capacity > 0:

                total += (
                    warehouse.current_utilization /
                    warehouse.capacity
                )

        return round(
            (total / len(warehouses)) * 100,
            2
        )
    @staticmethod
    def most_moved_products(db: Session):

        result = (
            db.query(
                InventoryTransaction.product_id
            )
            .group_by(
                InventoryTransaction.product_id
            )
            .count()
        )

        return result
    @staticmethod
    def inventory_analytics(db: Session):

        inventory = (
            db.query(
                Warehouse.warehouse_name.label("warehouse"),
                Product.product_name.label("product"),
                Inventory.available_quantity,
                Product.cost_price,
                (
                    Inventory.available_quantity *
                    Product.cost_price
                ).label("inventory_value")
            )
            .join(
                Warehouse,
                Warehouse.id == Inventory.warehouse_id
            )
            .join(
                Product,
                Product.id == Inventory.product_id
            )
            .all()
        )

        return inventory
    @staticmethod
    def supplier_analytics(db: Session):

        suppliers = (
            db.query(
                Supplier.supplier_name,

                func.count(PurchaseOrder.id)
                .label("purchase_orders"),

                func.sum(PurchaseOrder.total_amount)
                .label("total_purchase_value")
            )
            .outerjoin(
                PurchaseOrder,
                PurchaseOrder.supplier_id == Supplier.id
            )
            .group_by(
                Supplier.id
            )
            .all()
        )

        return suppliers
    @staticmethod
    def warehouse_analytics(db: Session):

        warehouses = (
            db.query(

                Warehouse.warehouse_name,

                Warehouse.capacity,

                Warehouse.current_utilization,

                (
                    Warehouse.current_utilization * 100.0 /
                    Warehouse.capacity
                ).label("utilization_percentage")

            )
            .all()
        )

        return warehouses