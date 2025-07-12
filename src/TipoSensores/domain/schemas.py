"""
Esquemas de validación y transferencia de datos para TipoSensor (Pydantic)
"""

from pydantic import BaseModel, Field


class TipoSensorBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: str

    class Config:
        from_attributes = True  # Permite trabajar con objetos de ORMs como SQLAlchemy


class TipoSensorCreate(TipoSensorBase):
    """Esquema para crear un nuevo tipo de sensor"""
    pass


class TipoSensorUpdate(BaseModel):
    """Esquema para actualizar un tipo de sensor"""
    nombre: str | None = Field(None, max_length=100)
    descripcion: str | None = None

    class Config:
        from_attributes = True


class TipoSensorResponse(TipoSensorBase):
    """Esquema de respuesta para mostrar un tipo de sensor"""
    id_tipo_sensor: int

    class Config:
        from_attributes = True
