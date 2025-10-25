"""
Middleware centralizado de autenticación JWT
Usado por todas las entidades de la aplicación
"""

from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.core.db import get_database
from src.Usuarios.application.auth_service import AuthService
from src.Usuarios.domain.schemas import UserResponse
from src.Usuarios.infrastructure.repositories import SqlAlchemyUserRepository

# Configuración de seguridad HTTP Bearer
security = HTTPBearer()
auth_service = AuthService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_database)
) -> UserResponse:
    """
    Middleware global para obtener usuario autenticado mediante JWT
    Usado en todas las entidades que requieren autenticación
    """
    try:
        token_data = auth_service.verify_token(credentials.credentials)
        repository = SqlAlchemyUserRepository(db)
        user = repository.get_by_id(token_data.user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        return user

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error de autenticación"
        )


def require_roles(allowed_roles: List[int]):
    """
    Factory para crear middleware de autorización por roles

    Args:
        allowed_roles: Lista de IDs de roles permitidos

    Usage:
        @router.get("/admin-only")
        def admin_endpoint(user = Depends(require_roles([1]))):  # Solo admin
    """
    def role_dependency(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
        if current_user.role_id not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Sin permisos. Roles requeridos: {allowed_roles}"
            )
        return current_user

    return role_dependency


# Middlewares preconfigurados para roles comunes
def require_admin():
    """Middleware que requiere rol de administrador (role_id = 1)"""
    return require_roles([1])


def require_admin_or_moderator():
    """Middleware que requiere rol de administrador o moderador"""
    return require_roles([1, 2])


def require_any_authenticated():
    """Middleware que requiere cualquier usuario autenticado"""
    return get_current_user


# Funciones auxiliares para verificar permisos en lógica de negocio
def user_can_modify_resource(current_user: UserResponse, resource_owner_id: int) -> bool:
    """
    Verificar si un usuario puede modificar un recurso
    - Admin puede modificar cualquier recurso
    - Usuario normal solo puede modificar sus propios recursos
    """
    return current_user.role_id == 1 or current_user.id == resource_owner_id


def user_has_role(current_user: UserResponse, required_roles: List[int]) -> bool:
    """Verificar si un usuario tiene alguno de los roles requeridos"""
    return current_user.role_id in required_roles
