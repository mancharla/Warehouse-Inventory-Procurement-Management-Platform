from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.repositories.supplier_repository import SupplierRepository


class SupplierService:

    @staticmethod
    def create(db: Session, data):

        if SupplierRepository.get_by_email(db, data.email):
            raise ValueError("Supplier email already exists")

        if SupplierRepository.get_by_gst(db, data.gst_number):
            raise ValueError("GST Number already exists")

        supplier = Supplier(
            supplier_name=data.supplier_name,
            contact_person=data.contact_person,
            email=data.email,
            phone=data.phone,
            gst_number=data.gst_number,
            address=data.address,
            rating=data.rating,
        )

        return SupplierRepository.create(db, supplier)

    @staticmethod
    def get_all(db: Session):
        return SupplierRepository.get_all(db)

    @staticmethod
    def get_by_id(db: Session, supplier_id):

        supplier = SupplierRepository.get_by_id(db, supplier_id)

        if supplier is None:
            raise ValueError("Supplier not found")

        return supplier
    @staticmethod
    def update(
        db: Session,
        supplier_id,
        data
    ):

        supplier = SupplierRepository.get_by_id(
            db,
            supplier_id
        )

        if supplier is None:
            raise ValueError("Supplier not found")

        if data.email:

            existing = SupplierRepository.get_by_email(
                db,
                data.email
            )

            if existing and existing.id != supplier.id:
                raise ValueError("Email already exists")

            supplier.email = data.email

        if data.gst_number:

            existing = SupplierRepository.get_by_gst(
                db,
                data.gst_number
            )

            if existing and existing.id != supplier.id:
                raise ValueError("GST already exists")

            supplier.gst_number = data.gst_number

        if data.supplier_name:
            supplier.supplier_name = data.supplier_name

        if data.contact_person:
            supplier.contact_person = data.contact_person

        if data.phone:
            supplier.phone = data.phone

        if data.address:
            supplier.address = data.address

        if data.rating is not None:
            supplier.rating = data.rating

        if data.is_active is not None:
            supplier.is_active = data.is_active

        return SupplierRepository.update(
            db,
            supplier
        )
    @staticmethod
    def suspend(
        db: Session,
        supplier_id
    ):

        supplier = SupplierRepository.get_by_id(
            db,
            supplier_id
        )

        if supplier is None:
            raise ValueError("Supplier not found")

        return SupplierRepository.suspend(
            db,
            supplier
        )
    @staticmethod
    def search(
        db: Session,
        search: str
    ):

        return SupplierRepository.search(
            db,
            search
        )
