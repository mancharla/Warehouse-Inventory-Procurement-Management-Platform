from celery import shared_task
from sqlalchemy.orm import Session
import asyncio

from app.database.database import SessionLocal

from app.models.inventory import Inventory

from app.services.inventory_alert_service import (
    InventoryAlertService,
)

from app.services.notification_service import (
    NotificationService,
)


# ============================================================
# INVENTORY RECONCILIATION
# ============================================================

@shared_task
def reconcile_inventory():

    db: Session = SessionLocal()

    try:

        inventories = (
            db.query(Inventory)
            .all()
        )

        fixed_records = 0

        for inventory in inventories:

            # ------------------------------------------------
            # Fix negative inventory
            # ------------------------------------------------

            if inventory.available_quantity < 0:

                inventory.available_quantity = 0

                fixed_records += 1

            # ------------------------------------------------
            # Generate inventory alerts
            # ------------------------------------------------

            InventoryAlertService.generate(
                db,
                inventory
            )

        # ----------------------------------------------------
        # Commit all inventory corrections
        # ----------------------------------------------------

        db.commit()

        # ----------------------------------------------------
        # Send ONE audit notification
        # ----------------------------------------------------

        try:

            asyncio.run(
                NotificationService.inventory_audit_due()
            )

        except Exception as e:

            print(
                "Inventory audit notification failed:",
                str(e)
            )

        return {
            "status": "success",
            "message": (
                "Inventory reconciliation completed"
            ),
            "checked_records": len(inventories),
            "fixed_records": fixed_records
        }

    except Exception as e:

        db.rollback()

        raise e

    finally:

        db.close()


# ============================================================
# LOW STOCK CHECK
# ============================================================

@shared_task
def check_low_stock():

    db: Session = SessionLocal()

    try:

        inventories = (
            db.query(Inventory)
            .all()
        )

        alert_count = 0

        for inventory in inventories:

            alert = InventoryAlertService.generate(
                db,
                inventory
            )

            if alert is not None:

                alert_count += 1

        db.commit()

        return {
            "status": "success",
            "message": (
                "Low stock check completed"
            ),
            "checked_records": len(inventories),
            "alerts_generated": alert_count
        }

    except Exception as e:

        db.rollback()

        raise e

    finally:

        db.close()


# ============================================================
# CLEANUP NEGATIVE STOCK
# ============================================================

@shared_task
def cleanup_negative_stock():

    db: Session = SessionLocal()

    try:

        inventories = (
            db.query(Inventory)
            .filter(
                Inventory.available_quantity < 0
            )
            .all()
        )

        count = 0

        for inventory in inventories:

            inventory.available_quantity = 0

            count += 1

        db.commit()

        return {
            "status": "success",
            "fixed_records": count
        }

    except Exception as e:

        db.rollback()

        raise e

    finally:

        db.close()