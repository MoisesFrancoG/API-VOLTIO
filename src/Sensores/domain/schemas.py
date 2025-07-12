"""
Esquemas de validación y transferencia de datos para Sensor (Pydantic)
"""

from pydantic import BaseModel, Field, validator
from typing import Optional

class SensorBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre del sensor")
    id_tipo_sensor: int = Field(..., gt=0, description="ID del tipo de sensor")
    id_ubicacion: int = Field(..., gt=0, description="ID de la ubicación")
    id_usuario: int = Field(..., gt=0, description="ID del usuario propietario")
    activo: bool = Field(True, description="Estado activo del sensor")

    @validator('nombre')
    def validar_nombre(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        if len(v.strip()) < 3:
            raise ValueError('El nombre debe tener al menos 3 caracteres')
        return v.strip()

    class Config:
        from_attributes = True


class SensorCreate(SensorBase):
    """Esquema para crear un nuevo sensor"""
    pass


class SensorUpdate(BaseModel):
    """Esquema para actualizar un sensor"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=100, description="Nombre del sensor")
    id_tipo_sensor: Optional[int] = Field(None, gt=0, description="ID del tipo de sensor")
    id_ubicacion: Optional[int] = Field(None, gt=0, description="ID de la ubicación")
    id_usuario: Optional[int] = Field(None, gt=0, description="ID del usuario propietario")
    activo: Optional[bool] = Field(None, description="Estado activo del sensor")

    @validator('nombre')
    def validar_nombre(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('El nombre no puede estar vacío')
            if len(v.strip()) < 3:
                raise ValueError('El nombre debe tener al menos 3 caracteres')
            return v.strip()
        return v

    class Config:
        from_attributes = True


class SensorResponse(SensorBase):
    """Esquema de respuesta para mostrar un sensor"""
    id_sensor: int

    class Config:
        from_attributes = True


class SensorEstadoUpdate(BaseModel):
    """Esquema para actualizar solo el estado del sensor"""
    activo: bool = Field(..., description="Estado activo del sensor")

    class Config:
        from_attributes = True
