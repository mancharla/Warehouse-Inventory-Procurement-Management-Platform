from celery import shared_task
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import SessionLocal

from app.models.inventory import Inventory
from app.models.purchase_order import PurchaseOrder
from app.models.stock_transfer import StockTransfer
from app.models.inventory_alert import InventoryAlert

from app.models.enums import (
    PurchaseOrderStatus,
    TransferStatus,
)


@shared_task
def generate_daily_inventory_report():

    db: Session = SessionLocal()

    try:

        total_products = db.query(Inventory).count()

        total_stock = (
            db.query(
                func.coalesce(
                    func.sum(
                        Inventory.available_quantity
                    ),
                    0
                )
            )
            .scalar()
        )

        low_stock_items = (
            db.query(InventoryAlert)
            .filter(
                InventoryAlert.is_acknowledged == False
            )
            .count()
        )

        return {

            "status": "success",

            "report": {

                "total_products": total_products,

                "total_available_stock": total_stock,

                "pending_alerts": low_stock_items
            }
        }

    except Exception as e:

        db.rollback()

        raise e

    finally:

        db.close()


@shared_task
def generate_procurement_report():

    db: Session = SessionLocal()

    try:

        total_purchase_orders = (
            db.query(PurchaseOrder)
            .count()
        )

        approved_purchase_orders = (
            db.query(PurchaseOrder)
            .filter(
                PurchaseOrder.status ==
                PurchaseOrderStatus.APPROVED
            )
            .count()
        )

        completed_purchase_orders = (
            db.query(PurchaseOrder)
            .filter(
                PurchaseOrder.status ==
                PurchaseOrderStatus.COMPLETED
            )
            .count()
        )

        total_purchase_value = (
            db.query(
                func.coalesce(
                    func.sum(
                        PurchaseOrder.total_amount
                    ),
                    0
                )
            )
            .scalar()
        )

        return {

            "status": "success",

            "report": {

                "total_purchase_orders":
                    total_purchase_orders,

                "approved_purchase_orders":
                    approved_purchase_orders,

                "completed_purchase_orders":
                    completed_purchase_orders,

                "total_purchase_value":
                    float(total_purchase_value)
            }
        }

    except Exception as e:

        db.rollback()

        raise e

    finally:

        db.close()


@shared_task
def generate_transfer_report():

    db: Session = SessionLocal()

    try:

        total_transfers = (
            db.query(StockTransfer)
            .count()
        )

        completed_transfers = (
            db.query(StockTransfer)
            .filter(
                StockTransfer.status ==
                TransferStatus.RECEIVED
            )
            .count()
        )

        pending_transfers = (
            db.query(StockTransfer)
            .filter(
                StockTransfer.status ==
                TransferStatus.REQUESTED
            )
            .count()
        )

        approved_transfers = (
            db.query(StockTransfer)
            .filter(
                StockTransfer.status ==
                TransferStatus.APPROVED
            )
            .count()
        )

        return {

            "status": "success",

            "report": {

                "total_transfers":
                    total_transfers,

                "completed_transfers":
                    completed_transfers,

                "approved_transfers":
                    approved_transfers,

                "pending_transfers":
                    pending_transfers
            }
        }

    except Exception as e:

        db.rollback()

        raise e

    finally:

        db.close()