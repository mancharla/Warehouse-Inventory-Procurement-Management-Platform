from sqlalchemy.orm import Session

from app.models.warehouse import Warehouse
from sqlalchemy import or_


class WarehouseRepository:

    @staticmethod
    def create(db: Session, warehouse: Warehouse):
        db.add(warehouse)
        db.commit()
        db.refresh(warehouse)
        return warehouse

    @staticmethod
    def get_all(db: Session):
        return db.query(Warehouse).all()

    @staticmethod
    def get_by_id(db: Session, warehouse_id):
        return (
            db.query(Warehouse)
            .filter(Warehouse.id == warehouse_id)
            .first()
        )

    @staticmethod
    def get_by_code(db: Session, code: str):
        return (
            db.query(Warehouse)
            .filter(Warehouse.code == code)
            .first()
        )

    @staticmethod
    def update(db: Session, warehouse: Warehouse):
        db.commit()
        db.refresh(warehouse)
        return warehouse

    @staticmethod
    def disable(db: Session, warehouse: Warehouse):
        warehouse.status = False
        db.commit()
        db.refresh(warehouse)
        return warehouse
    @staticmethod
    def search(
        db: Session,
        search: str
    ):

        return (
            db.query(Warehouse)
            .filter(
                or_(
                    Warehouse.warehouse_name.ilike(f"%{search}%"),
                    Warehouse.code.ilike(f"%{search}%")
                )
            )
            .all()
        )