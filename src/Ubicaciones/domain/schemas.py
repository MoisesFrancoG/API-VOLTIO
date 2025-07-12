"""
Esquemas de validación y transferencia de datos para Ubicacion (Pydantic)
"""

from pydantic import BaseModel, Field


class UbicacionBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: str

    class Config:
        from_attributes = True  # Permite trabajar con objetos de ORMs como SQLAlchemy


class UbicacionCreate(UbicacionBase):
    """Esquema para crear una nueva ubicación"""
    pass


class UbicacionUpdate(BaseModel):
    """Esquema para actualizar una ubicación"""
    nombre: str | None = Field(None, max_length=100)
    descripcion: str | None = None

    class Config:
        from_attributes = True


class UbicacionResponse(UbicacionBase):
    """Esquema de respuesta para mostrar una ubicación"""
    id_ubicacion: int

    class Config:
        from_attributes = True
