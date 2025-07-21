"""
Validation and data transfer schemas for DeviceType (Pydantic)
"""

from pydantic import BaseModel, Field


class DeviceTypeBase(BaseModel):
    type_name: str = Field(..., max_length=100)
    description: str | None = None

    class Config:
        from_attributes = True  # Allows working with ORM objects like SQLAlchemy


class DeviceTypeCreate(DeviceTypeBase):
    """Schema for creating a new device type"""
    pass


class DeviceTypeUpdate(BaseModel):
    """Schema for updating a device type"""
    type_name: str | None = Field(None, max_length=100)
    description: str | None = None

    class Config:
        from_attributes = True


class DeviceTypeResponse(DeviceTypeBase):
    """Response schema for displaying a device type"""
    id: int

    class Config:
        from_attributes = True
