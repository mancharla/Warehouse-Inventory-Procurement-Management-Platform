from uuid import UUID
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    sku: str = Field(..., min_length=2, max_length=50)
    product_name: str = Field(..., min_length=2, max_length=150)
    category: str = Field(..., min_length=2, max_length=100)
    brand: str = Field(..., min_length=2, max_length=100)
    unit: str = Field(..., min_length=1, max_length=30)
    cost_price: Decimal = Field(..., gt=0)
    selling_price: Decimal = Field(..., gt=0)
    reorder_level: int = Field(..., ge=0)
    barcode: Optional[str] = None


class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    product_name: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    unit: Optional[str] = None
    cost_price: Optional[Decimal] = Field(default=None, gt=0)
    selling_price: Optional[Decimal] = Field(default=None, gt=0)
    reorder_level: Optional[int] = Field(default=None, ge=0)
    barcode: Optional[str] = None
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    id: UUID
    sku: str
    product_name: str
    category: str
    brand: str
    unit: str
    cost_price: Decimal
    selling_price: Decimal
    reorder_level: int
    barcode: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True