"""
Rutas FastAPI para el módulo de Roles
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.db import get_database
from src.Roles.domain.schemas import RolCreate, RolUpdate, RolResponse
from src.Roles.application.use_cases import RolUseCases
from src.Roles.infrastructure.database import get_rol_use_cases


router = APIRouter(prefix="/roles", tags=["Roles"])


def get_use_cases(db: Session = Depends(get_database)) -> RolUseCases:
    """Dependency para obtener los casos de uso de Rol"""
    return get_rol_use_cases(db)


@router.get(
    "/",
    response_model=List[RolResponse],
    summary="Listar todos los roles",
    description="Obtiene una lista de todos los roles disponibles en el sistema"
)
def listar_roles(use_cases: RolUseCases = Depends(get_use_cases)):
    """Obtener todos los roles"""
    return use_cases.listar_roles()


@router.get(
    "/{id_rol}",
    response_model=RolResponse,
    summary="Obtener rol por ID",
    description="Obtiene un rol específico por su ID"
)
def obtener_rol(id_rol: int, use_cases: RolUseCases = Depends(get_use_cases)):
    """Obtener un rol por ID"""
    return use_cases.obtener_rol(id_rol)


@router.post(
    "/",
    response_model=RolResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo rol",
    description="Crea un nuevo rol en el sistema"
)
def crear_rol(rol: RolCreate, use_cases: RolUseCases = Depends(get_use_cases)):
    """Crear un nuevo rol"""
    return use_cases.crear_rol(rol)


@router.put(
    "/{id_rol}",
    response_model=RolResponse,
    summary="Actualizar rol",
    description="Actualiza un rol existente"
)
def actualizar_rol(
    id_rol: int,
    rol: RolUpdate,
    use_cases: RolUseCases = Depends(get_use_cases)
):
    """Actualizar un rol existente"""
    return use_cases.actualizar_rol(id_rol, rol)


@router.delete(
    "/{id_rol}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar rol",
    description="Elimina un rol del sistema"
)
def eliminar_rol(id_rol: int, use_cases: RolUseCases = Depends(get_use_cases)):
    """Eliminar un rol"""
    use_cases.eliminar_rol(id_rol)
    return {"message": "Rol eliminado exitosamente"}
