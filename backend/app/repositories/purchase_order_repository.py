
from sqlalchemy.orm import Session

from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_item import PurchaseOrderItem
from sqlalchemy import or_, cast, String
from app.models.supplier import Supplier

class PurchaseOrderRepository:

    @staticmethod
    def create_purchase_order(db: Session, purchase_order: PurchaseOrder):
        db.add(purchase_order)
        db.commit()
        db.refresh(purchase_order)
        return purchase_order

    @staticmethod
    def create_purchase_order_item(
        db: Session,
        purchase_order_item: PurchaseOrderItem
    ):
        db.add(purchase_order_item)
        db.commit()
        db.refresh(purchase_order_item)
        return purchase_order_item

    @staticmethod
    def get_all(db: Session):
        return db.query(PurchaseOrder).all()

    @staticmethod
    def get_by_id(db: Session, purchase_order_id):
        return (
            db.query(PurchaseOrder)
            .filter(PurchaseOrder.id == purchase_order_id)
            .first()
        )

    @staticmethod
    def update(db: Session, purchase_order: PurchaseOrder):
        db.commit()
        db.refresh(purchase_order)
        return purchase_order

    @staticmethod
    def delete(db: Session, purchase_order: PurchaseOrder):
        db.delete(purchase_order)
        db.commit()
    @staticmethod
    def get_by_po_number(db: Session, po_number: str):
        return (
            db.query(PurchaseOrder)
            .filter(PurchaseOrder.po_number == po_number)
            .first()
        )
    @staticmethod
    def get_items(db: Session, purchase_order_id):
        return (
            db.query(PurchaseOrderItem)
            .filter(
                PurchaseOrderItem.purchase_order_id == purchase_order_id
            )
            .all()
        )
    @staticmethod
    def search(
        db: Session,
        search: str

    ):
        return (
            db.query(PurchaseOrder)
            .join(
                Supplier,
                Supplier.id == PurchaseOrder.supplier_id
            )
            .filter(
                or_(
                    PurchaseOrder.po_number.ilike(
                        f"%{search}%"
                    ),

                    cast(
                        PurchaseOrder.status,
                        String
                    ).ilike(
                        f"%{search}%"
                    ),

                    Supplier.supplier_name.ilike(
                        f"%{search}%"
                    )
                )
            )
            .all()
        )
    @staticmethod
    def filter_purchase_orders(
        db: Session,
        status=None,
        supplier_id=None,
        warehouse_id=None,
        start_date=None,
        end_date=None
    ):

        query = db.query(PurchaseOrder)

        if status:
            query = query.filter(
                PurchaseOrder.status == status
            )

        if supplier_id:
            query = query.filter(
                PurchaseOrder.supplier_id == supplier_id
            )

        if warehouse_id:
            query = query.filter(
                PurchaseOrder.warehouse_id == warehouse_id
            )

        if start_date:
            query = query.filter(
                PurchaseOrder.order_date >= start_date
            )

        if end_date:
            query = query.filter(
                PurchaseOrder.order_date <= end_date
            )

        return query.all()