"""
Rutas FastAPI para el módulo de ComandosIR
"""

from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from src.core.db import get_database
from src.core.auth_middleware import get_current_user, require_admin, require_admin_or_moderator
from src.Usuarios.domain.schemas import UsuarioResponse
from src.ComandosIR.domain.schemas import ComandoIRCreate, ComandoIRUpdate, ComandoIRResponse
from src.ComandosIR.application.use_cases import ComandoIRUseCases
from src.ComandosIR.infrastructure.database import get_comando_ir_use_cases


router = APIRouter(prefix="/comandos-ir", tags=["Comandos IR"])


def get_use_cases(db: Session = Depends(get_database)) -> ComandoIRUseCases:
    """Dependency para obtener los casos de uso de ComandoIR"""
    return get_comando_ir_use_cases(db)


@router.get(
    "/",
    response_model=List[ComandoIRResponse],
    summary="Listar todos los comandos IR",
    description="Obtiene una lista de todos los comandos IR (requiere autenticación)"
)
def listar_comandos_ir(
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: ComandoIRUseCases = Depends(get_use_cases)
):
    """Obtener todos los comandos IR (requiere autenticación)"""
    return use_cases.listar_comandos_ir()


@router.get(
    "/sensor/{id_sensor}",
    response_model=List[ComandoIRResponse],
    summary="Listar comandos IR por sensor",
    description="Obtiene todos los comandos IR de un sensor específico (requiere autenticación)"
)
def listar_comandos_por_sensor(
    id_sensor: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: ComandoIRUseCases = Depends(get_use_cases)
):
    """Obtener todos los comandos IR de un sensor específico (requiere autenticación)"""
    return use_cases.obtener_comandos_por_sensor(id_sensor)


@router.get(
    "/{id_comando}",
    response_model=ComandoIRResponse,
    summary="Obtener comando IR por ID",
    description="Obtiene un comando IR específico por su ID (requiere autenticación)"
)
def obtener_comando_ir(
    id_comando: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: ComandoIRUseCases = Depends(get_use_cases)
):
    """Obtener un comando IR por ID (requiere autenticación)"""
    return use_cases.obtener_comando_ir(id_comando)


@router.post(
    "/",
    response_model=ComandoIRResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo comando IR",
    description="Crea un nuevo comando IR en el sistema (requiere permisos de admin o moderador)"
)
def crear_comando_ir(
    comando_ir: ComandoIRCreate,
    current_user: UsuarioResponse = Depends(require_admin_or_moderator()),
    use_cases: ComandoIRUseCases = Depends(get_use_cases)
):
    """Crear un nuevo comando IR (requiere admin o moderador)"""
    return use_cases.crear_comando_ir(comando_ir)


@router.put(
    "/{id_comando}",
    response_model=ComandoIRResponse,
    summary="Actualizar comando IR",
    description="Actualiza un comando IR existente (requiere permisos de admin o moderador)"
)
def actualizar_comando_ir(
    id_comando: int,
    comando_ir: ComandoIRUpdate,
    current_user: UsuarioResponse = Depends(require_admin_or_moderator()),
    use_cases: ComandoIRUseCases = Depends(get_use_cases)
):
    """Actualizar un comando IR existente (requiere admin o moderador)"""
    return use_cases.actualizar_comando_ir(id_comando, comando_ir)


@router.delete(
    "/{id_comando}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar comando IR",
    description="Elimina un comando IR del sistema (requiere permisos de administrador)"
)
def eliminar_comando_ir(
    id_comando: int,
    current_user: UsuarioResponse = Depends(require_admin()),
    use_cases: ComandoIRUseCases = Depends(get_use_cases)
):
    """Eliminar un comando IR (requiere admin)"""
    use_cases.eliminar_comando_ir(id_comando)
    return {"message": "Comando IR eliminado exitosamente"}
