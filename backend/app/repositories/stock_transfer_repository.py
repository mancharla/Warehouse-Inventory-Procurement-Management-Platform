from sqlalchemy.orm import Session

from app.models.stock_transfer import StockTransfer
from app.models.stock_transfer_item import StockTransferItem
from sqlalchemy import or_
from app.models.warehouse import Warehouse

class StockTransferRepository:

    @staticmethod
    def create_transfer(
        db: Session,
        transfer: StockTransfer
    ):
        db.add(transfer)
        db.commit()
        db.refresh(transfer)
        return transfer

    @staticmethod
    def create_transfer_item(
        db: Session,
        transfer_item: StockTransferItem
    ):
        db.add(transfer_item)
        db.commit()
        db.refresh(transfer_item)
        return transfer_item

    @staticmethod
    def get_all(db: Session):
        return db.query(StockTransfer).all()

    @staticmethod
    def get_by_id(
        db: Session,
        transfer_id
    ):
        return (
            db.query(StockTransfer)
            .filter(
                StockTransfer.id == transfer_id
            )
            .first()
        )

    @staticmethod
    def get_items(
        db: Session,
        transfer_id
    ):
        return (
            db.query(StockTransferItem)
            .filter(
                StockTransferItem.transfer_id == transfer_id
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        transfer: StockTransfer
    ):
        db.commit()
        db.refresh(transfer)
        return transfer

    @staticmethod
    def delete(
        db: Session,
        transfer: StockTransfer
    ):
        db.delete(transfer)
        db.commit()

    @staticmethod
    def search(
        db: Session,
        search: str
    ):

        return (
            db.query(StockTransfer)
            .join(
                Warehouse,
                StockTransfer.source_warehouse_id == Warehouse.id
            )
            .filter(
                or_(
                    StockTransfer.transfer_number.ilike(f"%{search}%"),
                    StockTransfer.status.ilike(f"%{search}%"),
                    Warehouse.warehouse_name.ilike(f"%{search}%")
                )
            )
            .all()
        )
        