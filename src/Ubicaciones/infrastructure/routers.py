"""
Rutas FastAPI para el módulo de Ubicaciones
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.db import get_database
from src.core.auth_middleware import get_current_user, require_admin, require_admin_or_moderator
from src.Usuarios.domain.schemas import UsuarioResponse
from src.Ubicaciones.domain.schemas import UbicacionCreate, UbicacionUpdate, UbicacionResponse
from src.Ubicaciones.application.use_cases import UbicacionUseCases
from src.Ubicaciones.infrastructure.database import get_ubicacion_use_cases


router = APIRouter(prefix="/ubicaciones", tags=["Ubicaciones"])


def get_use_cases(db: Session = Depends(get_database)) -> UbicacionUseCases:
    """Dependency para obtener los casos de uso de Ubicacion"""
    return get_ubicacion_use_cases(db)


@router.get(
    "/",
    response_model=List[UbicacionResponse],
    summary="Listar todas las ubicaciones",
    description="Obtiene una lista de todas las ubicaciones (requiere autenticación)"
)
def listar_ubicaciones(
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: UbicacionUseCases = Depends(get_use_cases)
):
    """Obtener todas las ubicaciones (requiere autenticación)"""
    return use_cases.listar_ubicaciones()


@router.get(
    "/{id_ubicacion}",
    response_model=UbicacionResponse,
    summary="Obtener ubicación por ID",
    description="Obtiene una ubicación específica por su ID (requiere autenticación)"
)
def obtener_ubicacion(
    id_ubicacion: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: UbicacionUseCases = Depends(get_use_cases)
):
    """Obtener una ubicación por ID (requiere autenticación)"""
    return use_cases.obtener_ubicacion(id_ubicacion)


@router.post(
    "/",
    response_model=UbicacionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva ubicación",
    description="Crea una nueva ubicación en el sistema (requiere permisos de admin o moderador)"
)
def crear_ubicacion(
    ubicacion: UbicacionCreate,
    current_user: UsuarioResponse = Depends(require_admin_or_moderator()),
    use_cases: UbicacionUseCases = Depends(get_use_cases)
):
    """Crear una nueva ubicación (requiere admin o moderador)"""
    return use_cases.crear_ubicacion(ubicacion)


@router.put(
    "/{id_ubicacion}",
    response_model=UbicacionResponse,
    summary="Actualizar ubicación",
    description="Actualiza una ubicación existente (requiere permisos de admin o moderador)"
)
def actualizar_ubicacion(
    id_ubicacion: int,
    ubicacion: UbicacionUpdate,
    current_user: UsuarioResponse = Depends(require_admin_or_moderator()),
    use_cases: UbicacionUseCases = Depends(get_use_cases)
):
    """Actualizar una ubicación existente (requiere admin o moderador)"""
    return use_cases.actualizar_ubicacion(id_ubicacion, ubicacion)


@router.delete(
    "/{id_ubicacion}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar ubicación",
    description="Elimina una ubicación del sistema (requiere permisos de administrador)"
)
def eliminar_ubicacion(
    id_ubicacion: int,
    current_user: UsuarioResponse = Depends(require_admin()),
    use_cases: UbicacionUseCases = Depends(get_use_cases)
):
    """Eliminar una ubicación (requiere admin)"""
    use_cases.eliminar_ubicacion(id_ubicacion)
    return {"message": "Ubicación eliminada exitosamente"}
