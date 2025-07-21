"""
Validation and data transfer schemas for DeviceCommand (Pydantic)
"""

from pydantic import BaseModel, Field


class DeviceCommandBase(BaseModel):
    device_capability_instance_id: int = Field(
        ..., gt=0, description="ID of the associated device capability instance")
    name: str = Field(..., max_length=100,
                      description="Name of the device command")
    description: str = Field(..., description="Description of the command")
    command_payload: str = Field(..., max_length=255,
                                 description="Command payload to execute")

    class Config:
        from_attributes = True  # Allows working with ORM objects like SQLAlchemy


class DeviceCommandCreate(DeviceCommandBase):
    """Schema for creating a new device command"""
    pass


class DeviceCommandUpdate(BaseModel):
    """Schema for updating a device command"""
    device_capability_instance_id: int | None = Field(
        None, gt=0, description="ID of the associated device capability instance")
    name: str | None = Field(None, max_length=100,
                             description="Name of the device command")
    description: str | None = Field(
        None, description="Description of the command")
    command_payload: str | None = Field(
        None, max_length=255, description="Command payload to execute")

    class Config:
        from_attributes = True


class DeviceCommandResponse(DeviceCommandBase):
    """Response schema for displaying a device command"""
    id: int

    class Config:
        from_attributes = True
