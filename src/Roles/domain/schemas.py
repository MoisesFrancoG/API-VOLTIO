"""
Esquemas de validación y transferencia de datos para Role (Pydantic)
"""

from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: str | None = None

    class Config:
        from_attributes = True  # Permite trabajar con objetos de ORMs como SQLAlchemy


class RoleCreate(RoleBase):
    """Esquema para crear un nuevo rol"""
    pass


class RoleUpdate(BaseModel):
    """Esquema para actualizar un rol"""
    name: str | None = Field(None, max_length=50)
    description: str | None = None

    class Config:
        from_attributes = True


class RoleResponse(RoleBase):
    """Esquema de respuesta para mostrar un rol"""
    id: int

    class Config:
        from_attributes = True
