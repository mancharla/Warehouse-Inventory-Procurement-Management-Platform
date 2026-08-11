from sqlalchemy.orm import Session

from app.models.product import Product
from sqlalchemy import or_
from app.models.product import Product

class ProductRepository:

    @staticmethod
    def create(db: Session, product: Product):
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_all(db: Session):
        return db.query(Product).all()

    @staticmethod
    def get_by_id(db: Session, product_id):
        return (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    @staticmethod
    def get_by_sku(db: Session, sku: str):
        return (
            db.query(Product)
            .filter(Product.sku == sku)
            .first()
        )

    @staticmethod
    def get_by_barcode(db: Session, barcode: str):
        return (
            db.query(Product)
            .filter(Product.barcode == barcode)
            .first()
        )

    @staticmethod
    def update(db: Session, product: Product):
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def archive(db: Session, product: Product):
        product.is_active = False
        db.commit()
        db.refresh(product)
        return product
    @staticmethod
    def search(
        db,
        search: str
    ):
        return (
            db.query(Product)
            .filter(
                or_(
                    Product.sku.ilike(f"%{search}%"),
                    Product.product_name.ilike(f"%{search}%"),
                    Product.category.ilike(f"%{search}%"),
                    Product.brand.ilike(f"%{search}%")
                )
            )
            .all()
        )
    @staticmethod
    def filter_products(
        db: Session,
        category: str = None,
        brand: str = None,
        is_active: bool = None
    ):

        query = db.query(Product)

        if category:
            query = query.filter(
                Product.category == category
            )

        if brand:
            query = query.filter(
                Product.brand == brand
            )

        if is_active is not None:
            query = query.filter(
                Product.is_active == is_active
            )

        return query.all()