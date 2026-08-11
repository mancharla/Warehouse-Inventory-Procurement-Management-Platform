from sqlalchemy.orm import Session

from app.models.inventory_alert import InventoryAlert


class InventoryAlertRepository:

    @staticmethod
    def create(
        db: Session,
        alert: InventoryAlert
    ):
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def get_all(db: Session):
        return db.query(InventoryAlert).all()

    @staticmethod
    def get_by_id(
        db: Session,
        alert_id
    ):
        return (
            db.query(InventoryAlert)
            .filter(
                InventoryAlert.id == alert_id
            )
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        alert: InventoryAlert
    ):
        db.commit()
        db.refresh(alert)
        return alert