"""
Esquemas de validación y transferencia de datos para Location (Pydantic)
"""

from pydantic import BaseModel, Field


class LocationBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str

    class Config:
        from_attributes = True  # Permite trabajar con objetos de ORMs como SQLAlchemy


class LocationCreate(LocationBase):
    """Esquema para crear una nueva ubicación"""
    pass


class LocationUpdate(BaseModel):
    """Esquema para actualizar una ubicación"""
    name: str | None = Field(None, max_length=100)
    description: str | None = None

    class Config:
        from_attributes = True


class LocationResponse(LocationBase):
    """Esquema de respuesta para mostrar una ubicación"""
    id: int

    class Config:
        from_attributes = True
