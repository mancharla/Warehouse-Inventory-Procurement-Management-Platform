from pydantic import BaseModel


class DashboardAnalyticsResponse(BaseModel):

    total_products: int

    total_warehouses: int

    inventory_value: float

    low_stock_items: int

    out_of_stock_items: int

    purchase_orders_this_month: int

    inventory_turnover: float

    supplier_performance: float

    warehouse_utilization: float

    most_moved_products: int

class InventoryAnalyticsResponse(BaseModel):

    warehouse: str

    product: str

    available_quantity: int

    cost_price: float

    inventory_value: float

    class Config:
        from_attributes = True


class SupplierAnalyticsResponse(BaseModel):

    supplier_name: str

    purchase_orders: int

    total_purchase_value: float | None

    class Config:
        from_attributes = True

class WarehouseAnalyticsResponse(BaseModel):

    warehouse_name: str

    capacity: int

    current_utilization: int

    utilization_percentage: float

    class Config:
        from_attributes = True