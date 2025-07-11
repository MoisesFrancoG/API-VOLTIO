"""
Esquemas de validación y transferencia de datos para Usuario (Pydantic)
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UsuarioBase(BaseModel):
    nombre_usuario: str = Field(..., min_length=1, max_length=100)
    correo: EmailStr = Field(..., max_length=100)
    id_rol: int = Field(..., gt=0)

    class Config:
        from_attributes = True


class UsuarioCreate(UsuarioBase):
    """Esquema para crear un nuevo usuario"""
    contrasena: str = Field(..., min_length=6, max_length=255)


class UsuarioUpdate(BaseModel):
    """Esquema para actualizar un usuario"""
    nombre_usuario: Optional[str] = Field(None, min_length=1, max_length=100)
    correo: Optional[EmailStr] = Field(None, max_length=100)
    id_rol: Optional[int] = Field(None, gt=0)

    class Config:
        from_attributes = True


class UsuarioUpdatePassword(BaseModel):
    """Esquema para actualizar contraseña"""
    contrasena_actual: str = Field(..., min_length=1)
    contrasena_nueva: str = Field(..., min_length=6, max_length=255)

    class Config:
        from_attributes = True


class UsuarioResponse(UsuarioBase):
    """Esquema de respuesta para mostrar un usuario"""
    id_usuario: int

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    """Esquema para login de usuario"""
    correo: EmailStr
    contrasena: str = Field(..., min_length=1)

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Esquema de respuesta para tokens JWT"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: int

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    """Datos contenidos en el token JWT"""
    user_id: Optional[int] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True
