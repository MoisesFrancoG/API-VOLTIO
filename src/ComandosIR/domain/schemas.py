"""
Esquemas de validación y transferencia de datos para ComandoIR (Pydantic)
"""

from pydantic import BaseModel, Field


class ComandoIRBase(BaseModel):
    id_sensor: int = Field(..., gt=0, description="ID del sensor asociado")
    nombre: str = Field(..., max_length=100, description="Nombre del comando IR")
    descripcion: str = Field(..., description="Descripción del comando")
    comando: str = Field(..., max_length=255, description="Comando IR a ejecutar")

    class Config:
        from_attributes = True  # Permite trabajar con objetos de ORMs como SQLAlchemy


class ComandoIRCreate(ComandoIRBase):
    """Esquema para crear un nuevo comando IR"""
    pass


class ComandoIRUpdate(BaseModel):
    """Esquema para actualizar un comando IR"""
    id_sensor: int | None = Field(None, gt=0, description="ID del sensor asociado")
    nombre: str | None = Field(None, max_length=100, description="Nombre del comando IR")
    descripcion: str | None = Field(None, description="Descripción del comando")
    comando: str | None = Field(None, max_length=255, description="Comando IR a ejecutar")

    class Config:
        from_attributes = True


class ComandoIRResponse(ComandoIRBase):
    """Esquema de respuesta para mostrar un comando IR"""
    id_comando: int

    class Config:
        from_attributes = True
