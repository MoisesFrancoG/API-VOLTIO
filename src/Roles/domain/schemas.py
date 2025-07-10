"""
Esquemas de validación y transferencia de datos para Rol (Pydantic)
"""

from pydantic import BaseModel, Field


class RolBase(BaseModel):
    nombre: str = Field(..., max_length=50)
    descripcion: str

    class Config:
        orm_mode = True  # Permite trabajar con objetos de ORMs como SQLAlchemy


class RolCreate(RolBase):
    """Esquema para crear un nuevo rol"""
    pass


class RolUpdate(BaseModel):
    """Esquema para actualizar un rol"""
    nombre: str | None = Field(None, max_length=50)
    descripcion: str | None = None

    class Config:
        orm_mode = True


class RolResponse(RolBase):
    """Esquema de respuesta para mostrar un rol"""
    id_rol: int
