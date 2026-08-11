from celery import shared_task
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import SessionLocal

from app.models.supplier import Supplier
from app.models.purchase_order import PurchaseOrder
from app.models.enums import PurchaseOrderStatus


@shared_task
def calculate_supplier_performance():

    db: Session = SessionLocal()

    try:

        suppliers = db.query(Supplier).all()

        report = []

        for supplier in suppliers:

            purchase_orders = (
                db.query(PurchaseOrder)
                .filter(
                    PurchaseOrder.supplier_id == supplier.id
                )
                .all()
            )

            total_orders = len(purchase_orders)

            completed_orders = len([
                po for po in purchase_orders
                if po.status == PurchaseOrderStatus.COMPLETED
            ])

            pending_orders = len([
                po for po in purchase_orders
                if po.status == PurchaseOrderStatus.PENDING_APPROVAL
            ])

            approved_orders = len([
                po for po in purchase_orders
                if po.status == PurchaseOrderStatus.APPROVED
            ])

            cancelled_orders = len([
                po for po in purchase_orders
                if po.status == PurchaseOrderStatus.CANCELLED
            ])

            total_amount = (
                db.query(
                    func.coalesce(
                        func.sum(PurchaseOrder.total_amount),
                        0
                    )
                )
                .filter(
                    PurchaseOrder.supplier_id == supplier.id
                )
                .scalar()
            )

            report.append({

                "supplier_id": str(supplier.id),

                "supplier_name": supplier.supplier_name,

                "total_orders": total_orders,

                "completed_orders": completed_orders,

                "approved_orders": approved_orders,

                "pending_orders": pending_orders,

                "cancelled_orders": cancelled_orders,

                "total_purchase_amount": float(total_amount)
            })

        return {

            "status": "success",

            "suppliers_processed": len(report),

            "data": report
        }

    except Exception as e:

        db.rollback()

        raise e

    finally:

        db.close()


@shared_task
def supplier_summary():

    db: Session = SessionLocal()

    try:

        total_suppliers = db.query(Supplier).count()

        active_suppliers = (
            db.query(Supplier)
            .filter(
                Supplier.is_active == True
            )
            .count()
        )

        inactive_suppliers = (
            total_suppliers -
            active_suppliers
        )

        return {

            "status": "success",

            "total_suppliers": total_suppliers,

            "active_suppliers": active_suppliers,

            "inactive_suppliers": inactive_suppliers
        }

    except Exception as e:

        raise e

    finally:

        db.close()