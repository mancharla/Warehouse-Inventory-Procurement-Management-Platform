import asyncio

from sqlalchemy.orm import Session

from app.models.inventory_alert import InventoryAlert
from app.models.enums import AlertType

from app.repositories.inventory_alert_repository import (
    InventoryAlertRepository,
)

from app.services.notification_service import (
    NotificationService,
)


class InventoryAlertService:

    # ============================================
    # GET ALL ALERTS
    # ============================================

    @staticmethod
    def get_all(
        db: Session
    ):

        return InventoryAlertRepository.get_all(
            db
        )

    # ============================================
    # ACKNOWLEDGE ALERT
    # ============================================

    @staticmethod
    def acknowledge(
        db: Session,
        alert_id
    ):

        alert = InventoryAlertRepository.get_by_id(
            db,
            alert_id
        )

        if alert is None:
            raise ValueError(
                "Alert not found"
            )

        alert.is_acknowledged = True

        return InventoryAlertRepository.update(
            db,
            alert
        )

    # ============================================
    # SEND LOW STOCK NOTIFICATION
    # ============================================

    @staticmethod
    def send_low_stock_notification(
        product_name,
        quantity
    ):

        try:

            loop = asyncio.get_running_loop()

            loop.create_task(
                NotificationService.low_stock(
                    product_name,
                    quantity
                )
            )

        except RuntimeError:

            # No running event loop.
            # The database alert is still created,
            # but WebSocket notification cannot be
            # sent from this synchronous context.
            pass

    # ============================================
    # GENERATE INVENTORY ALERT
    # ============================================

    @staticmethod
    def generate(
        db: Session,
        inventory
    ):

        product = inventory.product

        if product is None:
            return None

        # ========================================
        # OUT OF STOCK
        # ========================================

        if inventory.available_quantity == 0:

            alert = InventoryAlert(

                product_id=inventory.product_id,

                warehouse_id=inventory.warehouse_id,

                current_quantity=0,

                alert_type=AlertType.OUT_OF_STOCK,

                message=(
                    f"{product.product_name} "
                    f"is out of stock"
                )
            )

            alert = InventoryAlertRepository.create(
                db,
                alert
            )

            # ------------------------------------
            # WebSocket notification
            # ------------------------------------

            InventoryAlertService.send_low_stock_notification(
                product.product_name,
                inventory.available_quantity
            )

            return alert

        # ========================================
        # LOW STOCK
        # ========================================

        elif (
            inventory.available_quantity
            <= product.reorder_level
        ):

            alert = InventoryAlert(

                product_id=inventory.product_id,

                warehouse_id=inventory.warehouse_id,

                current_quantity=(
                    inventory.available_quantity
                ),

                alert_type=AlertType.LOW_STOCK,

                message=(
                    f"{product.product_name} "
                    f"reached reorder level"
                )
            )

            alert = InventoryAlertRepository.create(
                db,
                alert
            )

            # ------------------------------------
            # WebSocket notification
            # ------------------------------------

            InventoryAlertService.send_low_stock_notification(
                product.product_name,
                inventory.available_quantity
            )

            return alert

        # ========================================
        # OVER STOCK
        # ========================================

        elif inventory.available_quantity > 10000:

            alert = InventoryAlert(

                product_id=inventory.product_id,

                warehouse_id=inventory.warehouse_id,

                current_quantity=(
                    inventory.available_quantity
                ),

                alert_type=AlertType.OVER_STOCK,

                message=(
                    f"{product.product_name} "
                    f"is over stocked"
                )
            )

            alert = InventoryAlertRepository.create(
                db,
                alert
            )

            return alert

        # ========================================
        # NO ALERT
        # ========================================

        return None