from sqlalchemy.orm import Session

from app.repositories.analytics_repository import (
    AnalyticsRepository
)


class AnalyticsService:

    @staticmethod
    def dashboard(db: Session):

        return {

            "total_products":
            AnalyticsRepository.total_products(db),

            "total_warehouses":
            AnalyticsRepository.total_warehouses(db),

            "inventory_value":
            AnalyticsRepository.inventory_value(db),

            "low_stock_items":
            AnalyticsRepository.low_stock_items(db),

            "out_of_stock_items":
            AnalyticsRepository.out_of_stock_items(db),

            "purchase_orders_this_month":
            AnalyticsRepository.purchase_orders_this_month(db),

            "inventory_turnover":
            AnalyticsRepository.inventory_turnover(db),

            "supplier_performance":
            AnalyticsRepository.supplier_performance(db),

            "warehouse_utilization":
            AnalyticsRepository.warehouse_utilization(db),

            "most_moved_products":
            AnalyticsRepository.most_moved_products(db),
        }
    @staticmethod
    def inventory(db: Session):

        return AnalyticsRepository.inventory_analytics(db)
    @staticmethod
    def suppliers(db: Session):

        return AnalyticsRepository.supplier_analytics(db)   
    @staticmethod
    def warehouses(db: Session):

        return AnalyticsRepository.warehouse_analytics(db)