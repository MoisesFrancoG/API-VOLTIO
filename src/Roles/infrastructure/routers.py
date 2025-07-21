"""
Rutas FastAPI para el módulo de Roles
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.db import get_database
from src.core.auth_middleware import get_current_user, require_admin, require_admin_or_moderator
from src.Usuarios.domain.schemas import UserResponse
from src.Roles.domain.schemas import RoleCreate, RoleUpdate, RoleResponse
from src.Roles.application.use_cases import RoleUseCases
from src.Roles.infrastructure.database import get_role_use_cases


router = APIRouter(prefix="/roles", tags=["Roles"])


def get_use_cases(db: Session = Depends(get_database)) -> RoleUseCases:
    """Dependency para obtener los casos de uso de Role"""
    return get_role_use_cases(db)


@router.get(
    "/",
    response_model=List[RoleResponse],
    summary="Listar todos los roles",
    description="Obtiene una lista de todos los roles (requiere autenticación)"
)
def list_roles(
    current_user: UserResponse = Depends(get_current_user),
    use_cases: RoleUseCases = Depends(get_use_cases)
):
    """Obtener todos los roles (requiere autenticación)"""
    return use_cases.list_roles()


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Obtener rol por ID",
    description="Obtiene un rol específico por su ID (requiere autenticación)"
)
def get_role(
    role_id: int,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: RoleUseCases = Depends(get_use_cases)
):
    """Obtener un rol por ID (requiere autenticación)"""
    return use_cases.get_role(role_id)


@router.post(
    "/",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo rol",
    description="Crea un nuevo rol en el sistema (requiere permisos de admin)"
)
def create_role(
    role: RoleCreate,
    current_user: UserResponse = Depends(require_admin()),
    use_cases: RoleUseCases = Depends(get_use_cases)
):
    """Crear un nuevo rol (requiere solo admin)"""
    return use_cases.create_role(role)


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Actualizar rol",
    description="Actualiza un rol existente (requiere permisos de admin)"
)
def update_role(
    role_id: int,
    role: RoleUpdate,
    current_user: UserResponse = Depends(require_admin()),
    use_cases: RoleUseCases = Depends(get_use_cases)
):
    """Actualizar un rol existente (requiere solo admin)"""
    return use_cases.update_role(role_id, role)


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar rol",
    description="Elimina un rol del sistema (requiere permisos de administrador)"
)
def delete_role(
    role_id: int,
    current_user: UserResponse = Depends(require_admin()),
    use_cases: RoleUseCases = Depends(get_use_cases)
):
    """Eliminar un rol (requiere admin)"""
    use_cases.delete_role(role_id)
    return {"message": "Rol eliminado exitosamente"}
