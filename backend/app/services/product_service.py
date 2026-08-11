from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.product_repository import ProductRepository


class ProductService:

    @staticmethod
    def create(db: Session, data):

        if ProductRepository.get_by_sku(db, data.sku):
            raise ValueError("SKU already exists")

        if data.barcode:

            if ProductRepository.get_by_barcode(db, data.barcode):
                raise ValueError("Barcode already exists")

        if data.selling_price < data.cost_price:
            raise ValueError(
                "Selling price cannot be less than cost price"
            )

        product = Product(
            sku=data.sku,
            product_name=data.product_name,
            category=data.category,
            brand=data.brand,
            unit=data.unit,
            cost_price=data.cost_price,
            selling_price=data.selling_price,
            reorder_level=data.reorder_level,
            barcode=data.barcode,
        )

        return ProductRepository.create(db, product)

    @staticmethod
    def get_all(db: Session):
        return ProductRepository.get_all(db)

    @staticmethod
    def get_by_id(db: Session, product_id):

        product = ProductRepository.get_by_id(
            db,
            product_id
        )

        if product is None:
            raise ValueError("Product not found")

        return product
    @staticmethod
    def update(
        db: Session,
        product_id,
        data
    ):

        product = ProductRepository.get_by_id(
            db,
            product_id
        )

        if product is None:
            raise ValueError("Product not found")

        if data.sku:

            existing = ProductRepository.get_by_sku(
                db,
                data.sku
            )

            if existing and existing.id != product.id:
                raise ValueError("SKU already exists")

            product.sku = data.sku

        if data.barcode:

            existing = ProductRepository.get_by_barcode(
                db,
                data.barcode
            )

            if existing and existing.id != product.id:
                raise ValueError("Barcode already exists")

            product.barcode = data.barcode

        if data.product_name:
            product.product_name = data.product_name

        if data.category:
            product.category = data.category

        if data.brand:
            product.brand = data.brand

        if data.unit:
            product.unit = data.unit

        if data.cost_price is not None:
            product.cost_price = data.cost_price

        if data.selling_price is not None:
            product.selling_price = data.selling_price

        if (
            product.selling_price
            < product.cost_price
        ):
            raise ValueError(
                "Selling price cannot be less than cost price"
            )

        if data.reorder_level is not None:
            product.reorder_level = data.reorder_level

        if data.is_active is not None:
            product.is_active = data.is_active

        return ProductRepository.update(
            db,
            product
        )
    @staticmethod
    def archive(
                     db: Session,
                     product_id
                 ):
         
                     product = ProductRepository.get_by_id(
                         db,
                         product_id
                     )
         
                     if product is None:
                         raise ValueError("Product not found")
         
                     return ProductRepository.archive(
                         db,
                         product
                     )  
    @staticmethod
    def search(
        db,
        search: str
    ):
        return ProductRepository.search(
            db,
            search
        )   
    @staticmethod
    def filter_products(
        db: Session,
        category=None,
        brand=None,
        is_active=None
    ):

        return ProductRepository.filter_products(
            db,
            category,
            brand,
            is_active
        )  
    

        