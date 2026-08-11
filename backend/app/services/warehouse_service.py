from sqlalchemy.orm import Session

from app.models.warehouse import Warehouse
from app.models.enums import UserRole

from app.repositories.user_repository import UserRepository
from app.repositories.warehouse_repository import WarehouseRepository


class WarehouseService:

    @staticmethod
    def create(db: Session, data):

        existing = WarehouseRepository.get_by_code(
            db,
            data.code
        )

        if existing:
            raise ValueError("Warehouse code already exists")

        manager = None

        if data.manager_id:

            manager = UserRepository.get_by_id(
                db,
                data.manager_id
            )

            if manager is None:
                raise ValueError("Manager not found")

            if manager.role != UserRole.WAREHOUSE_MANAGER:
                raise ValueError(
                    "Assigned user must have WAREHOUSE_MANAGER role"
                )

        warehouse = Warehouse(
            warehouse_name=data.warehouse_name,
            code=data.code,
            address=data.address,
            capacity=data.capacity,
            manager_id=data.manager_id
        )

        return WarehouseRepository.create(
            db,
            warehouse
        )

    @staticmethod
    def get_all(db: Session):
        return WarehouseRepository.get_all(db)

    @staticmethod
    def get_by_id(db: Session, warehouse_id):

        warehouse = WarehouseRepository.get_by_id(
            db,
            warehouse_id
        )

        if warehouse is None:
            raise ValueError("Warehouse not found")

        return warehouse
    @staticmethod
    def update(
        db: Session,
        warehouse_id,
        data
    ):

        warehouse = WarehouseRepository.get_by_id(
            db,
            warehouse_id
        )

        if warehouse is None:
            raise ValueError("Warehouse not found")

        if data.code:

            existing = WarehouseRepository.get_by_code(
                db,
                data.code
            )

            if existing and existing.id != warehouse.id:
                raise ValueError(
                    "Warehouse code already exists"
                )

            warehouse.code = data.code

        if data.warehouse_name:
            warehouse.warehouse_name = data.warehouse_name

        if data.address:
            warehouse.address = data.address

        if data.capacity is not None:

            if data.capacity < warehouse.current_utilization:
                raise ValueError(
                    "Capacity cannot be less than current utilization"
                )

            warehouse.capacity = data.capacity

        if data.current_utilization is not None:

            if data.current_utilization > warehouse.capacity:
                raise ValueError(
                    "Current utilization exceeds capacity"
                )

            warehouse.current_utilization = data.current_utilization

        if data.manager_id:

            manager = UserRepository.get_by_id(
                db,
                data.manager_id
            )

            if manager is None:
                raise ValueError("Manager not found")

            if manager.role != UserRole.WAREHOUSE_MANAGER:
                raise ValueError(
                    "Assigned user must be Warehouse Manager"
                )

            warehouse.manager_id = data.manager_id

        if data.status is not None:
            warehouse.status = data.status

        return WarehouseRepository.update(
            db,
            warehouse
        )
    @staticmethod
    def disable(
        db: Session,
        warehouse_id
    ):

        warehouse = WarehouseRepository.get_by_id(
            db,
            warehouse_id
        )

        if warehouse is None:
            raise ValueError("Warehouse not found")

        return WarehouseRepository.disable(
            db,
            warehouse
        )
    @staticmethod
    def assign_manager(
        db: Session,
        warehouse_id,
        manager_id
    ):

        warehouse = WarehouseRepository.get_by_id(
            db,
            warehouse_id
        )

        if warehouse is None:
            raise ValueError("Warehouse not found")

        manager = UserRepository.get_by_id(
            db,
            manager_id
        )

        if manager is None:
            raise ValueError("Manager not found")

        if manager.role != UserRole.WAREHOUSE_MANAGER:
            raise ValueError(
                "Assigned user must have WAREHOUSE_MANAGER role"
            )

        warehouse.manager_id = manager_id

        return WarehouseRepository.update(
            db,
            warehouse
        )
    @staticmethod
    def search(
        db: Session,
        search: str
    ):

        return WarehouseRepository.search(
            db,
            search
        )