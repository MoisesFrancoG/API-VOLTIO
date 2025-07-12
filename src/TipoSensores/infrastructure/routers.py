"""
Rutas FastAPI para el módulo de TipoSensores
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.db import get_database
from src.core.auth_middleware import get_current_user, require_admin, require_admin_or_moderator
from src.Usuarios.domain.schemas import UsuarioResponse
from src.TipoSensores.domain.schemas import TipoSensorCreate, TipoSensorUpdate, TipoSensorResponse
from src.TipoSensores.application.use_cases import TipoSensorUseCases
from src.TipoSensores.infrastructure.database import get_tipo_sensor_use_cases


router = APIRouter(prefix="/tipo-sensores", tags=["Tipo Sensores"])


def get_use_cases(db: Session = Depends(get_database)) -> TipoSensorUseCases:
    """Dependency para obtener los casos de uso de TipoSensor"""
    return get_tipo_sensor_use_cases(db)


@router.get(
    "/",
    response_model=List[TipoSensorResponse],
    summary="Listar todos los tipos de sensores",
    description="Obtiene una lista de todos los tipos de sensores (requiere autenticación)"
)
def listar_tipos_sensores(
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: TipoSensorUseCases = Depends(get_use_cases)
):
    """Obtener todos los tipos de sensores (requiere autenticación)"""
    return use_cases.listar_tipos_sensores()


@router.get(
    "/{id_tipo_sensor}",
    response_model=TipoSensorResponse,
    summary="Obtener tipo de sensor por ID",
    description="Obtiene un tipo de sensor específico por su ID (requiere autenticación)"
)
def obtener_tipo_sensor(
    id_tipo_sensor: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: TipoSensorUseCases = Depends(get_use_cases)
):
    """Obtener un tipo de sensor por ID (requiere autenticación)"""
    return use_cases.obtener_tipo_sensor(id_tipo_sensor)


@router.post(
    "/",
    response_model=TipoSensorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo tipo de sensor",
    description="Crea un nuevo tipo de sensor en el sistema (requiere permisos de admin o moderador)"
)
def crear_tipo_sensor(
    tipo_sensor: TipoSensorCreate,
    current_user: UsuarioResponse = Depends(require_admin_or_moderator()),
    use_cases: TipoSensorUseCases = Depends(get_use_cases)
):
    """Crear un nuevo tipo de sensor (requiere admin o moderador)"""
    return use_cases.crear_tipo_sensor(tipo_sensor)


@router.put(
    "/{id_tipo_sensor}",
    response_model=TipoSensorResponse,
    summary="Actualizar tipo de sensor",
    description="Actualiza un tipo de sensor existente (requiere permisos de admin o moderador)"
)
def actualizar_tipo_sensor(
    id_tipo_sensor: int,
    tipo_sensor: TipoSensorUpdate,
    current_user: UsuarioResponse = Depends(require_admin_or_moderator()),
    use_cases: TipoSensorUseCases = Depends(get_use_cases)
):
    """Actualizar un tipo de sensor existente (requiere admin o moderador)"""
    return use_cases.actualizar_tipo_sensor(id_tipo_sensor, tipo_sensor)


@router.delete(
    "/{id_tipo_sensor}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar tipo de sensor",
    description="Elimina un tipo de sensor del sistema (requiere permisos de administrador)"
)
def eliminar_tipo_sensor(
    id_tipo_sensor: int,
    current_user: UsuarioResponse = Depends(require_admin()),
    use_cases: TipoSensorUseCases = Depends(get_use_cases)
):
    """Eliminar un tipo de sensor (requiere admin)"""
    use_cases.eliminar_tipo_sensor(id_tipo_sensor)
    return {"message": "Tipo de sensor eliminado exitosamente"}
