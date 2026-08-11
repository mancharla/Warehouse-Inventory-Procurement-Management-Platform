from celery import shared_task
from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.models.inventory import Inventory

from app.services.inventory_alert_service import (
    InventoryAlertService,
)


@shared_task
def generate_inventory_alerts():

    db: Session = SessionLocal()

    try:

        inventories = db.query(Inventory).all()

        alerts_generated = 0

        for inventory in inventories:

            InventoryAlertService.generate(
                db,
                inventory
            )

            alerts_generated += 1

        return {

            "status": "success",

            "message": "Inventory alerts generated",

            "processed_records": alerts_generated
        }

    except Exception as e:

        db.rollback()

        raise e

    finally:

        db.close()


@shared_task
def check_out_of_stock():

    db: Session = SessionLocal()

    try:

        inventories = (
            db.query(Inventory)
            .filter(
                Inventory.available_quantity == 0
            )
            .all()
        )

        count = 0

        for inventory in inventories:

            InventoryAlertService.generate(
                db,
                inventory
            )

            count += 1

        return {

            "status": "success",

            "out_of_stock_products": count
        }

    except Exception as e:

        db.rollback()

        raise e

    finally:

        db.close()


@shared_task
def check_over_stock():

    db: Session = SessionLocal()

    try:

        inventories = (
            db.query(Inventory)
            .filter(
                Inventory.available_quantity > 10000
            )
            .all()
        )

        count = 0

        for inventory in inventories:

            InventoryAlertService.generate(
                db,
                inventory
            )

            count += 1

        return {

            "status": "success",

            "over_stock_products": count
        }

    except Exception as e:

        db.rollback()

        raise e

    finally:

        db.close()