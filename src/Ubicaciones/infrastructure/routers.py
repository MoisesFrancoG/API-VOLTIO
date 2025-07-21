"""
Rutas FastAPI para el módulo de Locations
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.db import get_database
from src.core.auth_middleware import get_current_user, require_admin, require_admin_or_moderator
from src.Usuarios.domain.schemas import UserResponse
from src.Ubicaciones.domain.schemas import LocationCreate, LocationUpdate, LocationResponse
from src.Ubicaciones.application.use_cases import LocationUseCases
from src.Ubicaciones.infrastructure.database import get_location_use_cases


router = APIRouter(prefix="/locations", tags=["Locations"])


def get_use_cases(db: Session = Depends(get_database)) -> LocationUseCases:
    """Dependency para obtener los casos de uso de Location"""
    return get_location_use_cases(db)


@router.get(
    "/",
    response_model=List[LocationResponse],
    summary="Listar todas las ubicaciones",
    description="Obtiene una lista de todas las ubicaciones (requiere autenticación)"
)
def list_locations(
    current_user: UserResponse = Depends(get_current_user),
    use_cases: LocationUseCases = Depends(get_use_cases)
):
    """Obtener todas las ubicaciones (requiere autenticación)"""
    return use_cases.list_locations()


@router.get(
    "/{location_id}",
    response_model=LocationResponse,
    summary="Obtener ubicación por ID",
    description="Obtiene una ubicación específica por su ID (requiere autenticación)"
)
def get_location(
    location_id: int,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: LocationUseCases = Depends(get_use_cases)
):
    """Obtener una ubicación por ID (requiere autenticación)"""
    return use_cases.get_location(location_id)


@router.post(
    "/",
    response_model=LocationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva ubicación",
    description="Crea una nueva ubicación en el sistema (requiere permisos de admin)"
)
def create_location(
    location: LocationCreate,
    current_user: UserResponse = Depends(require_admin()),
    use_cases: LocationUseCases = Depends(get_use_cases)
):
    """Crear una nueva ubicación (requiere solo admin)"""
    return use_cases.create_location(location)


@router.put(
    "/{location_id}",
    response_model=LocationResponse,
    summary="Actualizar ubicación",
    description="Actualiza una ubicación existente (requiere permisos de admin)"
)
def update_location(
    location_id: int,
    location: LocationUpdate,
    current_user: UserResponse = Depends(require_admin()),
    use_cases: LocationUseCases = Depends(get_use_cases)
):
    """Actualizar una ubicación existente (requiere solo admin)"""
    return use_cases.update_location(location_id, location)


@router.delete(
    "/{location_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar ubicación",
    description="Elimina una ubicación del sistema (requiere permisos de administrador)"
)
def delete_location(
    location_id: int,
    current_user: UserResponse = Depends(require_admin()),
    use_cases: LocationUseCases = Depends(get_use_cases)
):
    """Eliminar una ubicación (requiere admin)"""
    use_cases.delete_location(location_id)
    return {"message": "Ubicación eliminada exitosamente"}
