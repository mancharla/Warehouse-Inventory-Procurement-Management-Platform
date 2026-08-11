from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


class WarehouseCreate(BaseModel):
    warehouse_name: str = Field(..., min_length=3, max_length=150)
    code: str = Field(..., min_length=2, max_length=30)
    address: str
    capacity: int = Field(..., gt=0)
    manager_id: Optional[UUID] = None


class WarehouseUpdate(BaseModel):
    warehouse_name: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None
    capacity: Optional[int] = Field(default=None, gt=0)
    current_utilization: Optional[int] = Field(default=None, ge=0)
    manager_id: Optional[UUID] = None
    status: Optional[bool] = None


class WarehouseResponse(BaseModel):
    id: UUID
    warehouse_name: str
    code: str
    address: str
    capacity: int
    current_utilization: int
    status: bool
    manager_id: Optional[UUID]

    class Config:
        from_attributes = True
        
class AssignManagerRequest(BaseModel):
    manager_id: UUID