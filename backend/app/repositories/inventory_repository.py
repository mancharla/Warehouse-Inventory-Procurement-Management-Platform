from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.inventory_transaction import InventoryTransaction
from sqlalchemy import or_
from app.models.product import Product
from app.models.warehouse import Warehouse

class InventoryRepository:

    @staticmethod
    def get_inventory(db: Session, product_id, warehouse_id):
        return (
            db.query(Inventory)
            .filter(
                Inventory.product_id == product_id,
                Inventory.warehouse_id == warehouse_id
            )
            .first()
        )

    @staticmethod
    def create_inventory(db: Session, inventory: Inventory):
        db.add(inventory)
        db.commit()
        db.refresh(inventory)
        return inventory

    @staticmethod
    def update_inventory(db: Session, inventory: Inventory):
        db.commit()
        db.refresh(inventory)
        return inventory

    @staticmethod
    def get_all(db: Session):
        return db.query(Inventory).all()

    @staticmethod
    def add_transaction(
        db: Session,
        transaction: InventoryTransaction
    ):
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def get_history(db: Session):
        return (
            db.query(InventoryTransaction)
            .order_by(
                InventoryTransaction.created_at.desc()
            )
            .all()
        )
    @staticmethod
    def search(
        db: Session,
        search: str
    ):

        return (
            db.query(Inventory)
            .join(Product)
            .join(Warehouse)
            .filter(
                or_(
                    Product.product_name.ilike(f"%{search}%"),
                    Product.sku.ilike(f"%{search}%"),
                    Warehouse.warehouse_name.ilike(f"%{search}%")
                )
            )
            .all()
        )
    @staticmethod
    def filter_inventory(
        db: Session,
        warehouse_id=None,
        product_id=None,
        low_stock: bool = False,
        out_of_stock: bool = False
    ):

        query = (
            db.query(Inventory)
            .join(Product)
        )

        if warehouse_id:
            query = query.filter(
                Inventory.warehouse_id == warehouse_id
            )

        if product_id:
            query = query.filter(
                Inventory.product_id == product_id
            )

        if low_stock:
            query = query.filter(
                Inventory.available_quantity <= Product.reorder_level,
                Inventory.available_quantity > 0
            )

        if out_of_stock:
            query = query.filter(
                Inventory.available_quantity == 0
            )

        return query.all()
        