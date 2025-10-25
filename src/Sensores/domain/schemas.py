"""
Validation and data transfer schemas for Device (Pydantic)
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100,
                      description="Device name")
    device_type_id: int = Field(..., gt=0, description="Device type ID")
    user_id: int = Field(..., gt=0, description="Owner user ID")
    is_active: bool = Field(True, description="Device active status")
    mac_address: str = Field(..., min_length=12, max_length=17,
                             description="MAC address of the device")
    description: Optional[str] = Field(None, description="Device description")

    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Device name cannot be empty')
        return v.strip()

    @validator('mac_address')
    def validate_mac_address(cls, v):
        if not v or not v.strip():
            raise ValueError('MAC address cannot be empty')

        # Remover separadores y convertir a mayúsculas
        clean_mac = v.strip().replace(':', '').replace('-', '').replace(' ', '').upper()

        # Validar longitud
        if len(clean_mac) != 12:
            raise ValueError('MAC address must be 12 hex characters')

        # Validar que solo contenga caracteres hexadecimales
        try:
            int(clean_mac, 16)
        except ValueError:
            raise ValueError(
                'MAC address must contain only hexadecimal characters')

        # Formatear correctamente con dos puntos
        formatted_mac = ':'.join([clean_mac[i:i+2] for i in range(0, 12, 2)])
        return formatted_mac

    class Config:
        from_attributes = True


class DeviceCreate(BaseModel):
    """Schema for creating a new device - user_id taken from auth"""
    name: str = Field(..., min_length=3, max_length=100,
                      description="Device name")
    device_type_id: int = Field(..., gt=0, description="Device type ID")
    is_active: bool = Field(True, description="Device active status")
    mac_address: str = Field(..., min_length=12, max_length=17,
                             description="MAC address of the device")
    description: Optional[str] = Field(None, description="Device description")

    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Device name cannot be empty')
        return v.strip()

    @validator('mac_address')
    def validate_mac_address(cls, v):
        if not v or not v.strip():
            raise ValueError('MAC address cannot be empty')

        # Remover separadores y convertir a mayúsculas
        clean_mac = v.strip().replace(':', '').replace('-', '').replace(' ', '')

        # Validar longitud
        if len(clean_mac) != 12:
            raise ValueError('MAC address must be 12 hex characters')

        # Validar que solo contenga caracteres hexadecimales
        try:
            int(clean_mac, 16)
        except ValueError:
            raise ValueError(
                'MAC address must contain only hexadecimal characters')

        # Formatear correctamente con dos puntos
        formatted_mac = ':'.join([clean_mac[i:i+2] for i in range(0, 12, 2)])
        return formatted_mac

    class Config:
        from_attributes = True


class DeviceUpdate(BaseModel):
    """Schema for updating a device"""
    name: str | None = Field(
        None, min_length=3, max_length=100, description="Device name")
    device_type_id: int | None = Field(
        None, gt=0, description="Device type ID")
    user_id: int | None = Field(None, gt=0, description="Owner user ID")
    is_active: bool | None = Field(None, description="Device active status")
    mac_address: str | None = Field(
        None, min_length=12, max_length=17, description="MAC address")
    description: str | None = Field(None, description="Device description")

    @validator('name')
    def validate_name(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Device name cannot be empty')
        return v.strip() if v else v

    @validator('mac_address')
    def validate_mac_address(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('MAC address cannot be empty')

            # Remover separadores y convertir a mayúsculas
            clean_mac = v.strip().replace(':', '').replace('-', '').replace(' ', '').upper()

            # Validar longitud
            if len(clean_mac) != 12:
                raise ValueError('MAC address must be 12 hex characters')

            # Validar que solo contenga caracteres hexadecimales
            try:
                int(clean_mac, 16)
            except ValueError:
                raise ValueError(
                    'MAC address must contain only hexadecimal characters')

            # Formatear correctamente con dos puntos
            formatted_mac = ':'.join([clean_mac[i:i+2]
                                     for i in range(0, 12, 2)])
            return formatted_mac
        return v

    class Config:
        from_attributes = True


class DeviceResponse(BaseModel):
    """Response schema for displaying a device"""
    id: int
    name: str
    device_type_id: int
    user_id: int
    is_active: bool = Field(default=True)
    mac_address: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    class Config:
        from_attributes = True


class DeviceStatusUpdate(BaseModel):
    """Schema for updating device status"""
    is_active: bool = Field(..., description="New device status")

    class Config:
        from_attributes = True


class DeviceSummary(BaseModel):
    """Summary schema for device statistics"""
    total_devices: int
    active_devices: int
    inactive_devices: int

    class Config:
        from_attributes = True


# Schemas for Relay Command Endpoint
class RelayCommandRequest(BaseModel):
    """Schema for relay command request"""
    action: str = Field(..., description="Relay action: ON or OFF")

    @validator('action')
    def validate_action(cls, v):
        if v not in ['ON', 'OFF']:
            raise ValueError("Action must be 'ON' or 'OFF'")
        return v

    class Config:
        from_attributes = True


class RelayCommandResponse(BaseModel):
    """Schema for relay command response"""
    status: str
    device_mac: str
    action_sent: str

    class Config:
        from_attributes = True
