"""
Esquemas de validación y transferencia de datos para Lectura (Pydantic)
"""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class LecturaBase(BaseModel):
    id_sensor: int = Field(..., gt=0, description="ID del sensor asociado")
    valor: float = Field(..., ge=0, description="Valor de la lectura")
    unidad: str = Field(..., max_length=10, description="Unidad de medida")
    fecha_hora: Optional[datetime] = Field(None, description="Fecha y hora de la lectura")

    @validator('unidad')
    def validar_unidad(cls, v):
        unidades_validas = ["°C", "°F", "V", "A", "W", "kW", "kWh", "%", "ppm", "bar", "Pa", "m/s", "Hz"]
        if v not in unidades_validas:
            raise ValueError(f'La unidad debe ser una de: {", ".join(unidades_validas)}')
        return v

    @validator('fecha_hora', pre=True, always=True)
    def set_fecha_hora(cls, v):
        return v or datetime.now()

    class Config:
        from_attributes = True  # Permite trabajar con objetos de ORMs como SQLAlchemy


class LecturaCreate(LecturaBase):
    """Esquema para crear una nueva lectura"""
    pass


class LecturaUpdate(BaseModel):
    """Esquema para actualizar una lectura"""
    id_sensor: Optional[int] = Field(None, gt=0, description="ID del sensor asociado")
    valor: Optional[float] = Field(None, ge=0, description="Valor de la lectura")
    unidad: Optional[str] = Field(None, max_length=10, description="Unidad de medida")

    @validator('unidad')
    def validar_unidad(cls, v):
        if v is not None:
            unidades_validas = ["°C", "°F", "V", "A", "W", "kW", "kWh", "%", "ppm", "bar", "Pa", "m/s", "Hz"]
            if v not in unidades_validas:
                raise ValueError(f'La unidad debe ser una de: {", ".join(unidades_validas)}')
            return v
        return v

    class Config:
        from_attributes = True


class LecturaResponse(LecturaBase):
    """Esquema de respuesta para mostrar una lectura"""
    id_lectura: int
    fecha_hora: datetime

    class Config:
        from_attributes = True
