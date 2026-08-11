from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from sqlalchemy import or_

class SupplierRepository:

    @staticmethod
    def create(db: Session, supplier: Supplier):
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        return supplier

    @staticmethod
    def get_all(db: Session):
        return db.query(Supplier).all()

    @staticmethod
    def get_by_id(db: Session, supplier_id):
        return (
            db.query(Supplier)
            .filter(Supplier.id == supplier_id)
            .first()
        )

    @staticmethod
    def get_by_email(db: Session, email: str):
        return (
            db.query(Supplier)
            .filter(Supplier.email == email)
            .first()
        )

    @staticmethod
    def get_by_gst(db: Session, gst: str):
        return (
            db.query(Supplier)
            .filter(Supplier.gst_number == gst)
            .first()
        )

    @staticmethod
    def update(db: Session, supplier: Supplier):
        db.commit()
        db.refresh(supplier)
        return supplier

    @staticmethod
    def suspend(db: Session, supplier: Supplier):
        supplier.is_active = False
        db.commit()
        db.refresh(supplier)
        return supplier
    @staticmethod
    def search(
        db: Session,
        search: str
    ):

        return (
            db.query(Supplier)
            .filter(
                or_(
                    Supplier.supplier_name.ilike(f"%{search}%"),
                    Supplier.contact_person.ilike(f"%{search}%"),
                    Supplier.email.ilike(f"%{search}%"),
                    Supplier.gst_number.ilike(f"%{search}%")
                )
            )
            .all()
        )