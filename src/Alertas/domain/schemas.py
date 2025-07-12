"""
Esquemas de validación y transferencia de datos para Alerta (Pydantic)
"""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class AlertaBase(BaseModel):
    id_lectura: int = Field(..., gt=0, description="ID de la lectura asociada")
    tipo_alerta: str = Field(..., max_length=100, description="Tipo de alerta")
    descripcion: str = Field(..., min_length=5, description="Descripción de la alerta")
    fecha_hora: Optional[datetime] = Field(None, description="Fecha y hora de la alerta")
    """
    @validator('tipo_alerta')
    def validar_tipo_alerta(cls, v):
        tipos_validos = ["CRITICA", "ADVERTENCIA", "INFO", "ERROR", "MANTENIMIENTO"]
        if v.upper() not in tipos_validos:
            raise ValueError(f'El tipo de alerta debe ser uno de: {", ".join(tipos_validos)}')
        return v.upper()
    """
    @validator('fecha_hora', pre=True, always=True)
    def set_fecha_hora(cls, v):
        return v or datetime.now()

    class Config:
        from_attributes = True  # Permite trabajar con objetos de ORMs como SQLAlchemy


class AlertaCreate(AlertaBase):
    """Esquema para crear una nueva alerta"""
    pass


class AlertaUpdate(BaseModel):
    """Esquema para actualizar una alerta"""
    id_lectura: Optional[int] = Field(None, gt=0, description="ID de la lectura asociada")
    tipo_alerta: Optional[str] = Field(None, max_length=100, description="Tipo de alerta")
    descripcion: Optional[str] = Field(None, min_length=5, description="Descripción de la alerta")

    @validator('tipo_alerta')
    def validar_tipo_alerta(cls, v):
        if v is not None:
            tipos_validos = ["CRITICA", "ADVERTENCIA", "INFO", "ERROR", "MANTENIMIENTO"]
            if v.upper() not in tipos_validos:
                raise ValueError(f'El tipo de alerta debe ser uno de: {", ".join(tipos_validos)}')
            return v.upper()
        return v

    class Config:
        from_attributes = True


class AlertaResponse(AlertaBase):
    """Esquema de respuesta para mostrar una alerta"""
    id_alerta: int
    fecha_hora: datetime

    class Config:
        from_attributes = True
