"""
Esquemas de validación y transferencia de datos para User (Pydantic)
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., max_length=100)
    role_id: int = Field(default=2, gt=0)  # Default USER role (regular users)

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    """Esquema para crear un nuevo usuario"""
    password: str = Field(..., min_length=6, max_length=255)
    role_id: int = Field(default=2, gt=0)  # Default: Regular USER role (ID=2)


class UserUpdate(BaseModel):
    """Esquema para actualizar un usuario"""
    username: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = Field(None, max_length=100)
    role_id: Optional[int] = Field(None, gt=0)

    class Config:
        from_attributes = True


class UserUpdatePassword(BaseModel):
    """Esquema para actualizar contraseña"""
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6, max_length=255)

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """Esquema de respuesta para mostrar un usuario"""
    id: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Esquema para login de usuario"""
    email: EmailStr
    password: str = Field(..., min_length=1)

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


class UserTokenData(BaseModel):
    """Datos contenidos en el token JWT"""
    user_id: Optional[int] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True
