from uuid import UUID
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class SupplierCreate(BaseModel):
    supplier_name: str = Field(..., min_length=3, max_length=150)
    contact_person: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    gst_number: str = Field(..., min_length=15, max_length=20)
    address: str
    rating: float = Field(default=5.0, ge=0, le=5)


class SupplierUpdate(BaseModel):
    supplier_name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    gst_number: Optional[str] = None
    address: Optional[str] = None
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    is_active: Optional[bool] = None


class SupplierResponse(BaseModel):
    id: UUID
    supplier_name: str
    contact_person: str
    email: EmailStr
    phone: str
    gst_number: str
    address: str
    rating: float
    is_active: bool

    class Config:
        from_attributes = True