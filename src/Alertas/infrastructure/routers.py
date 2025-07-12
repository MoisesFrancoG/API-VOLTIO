"""
Rutas FastAPI para el módulo de Alertas
"""

from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from src.core.db import get_database
from src.core.auth_middleware import get_current_user, require_admin, require_admin_or_moderator
from src.Usuarios.domain.schemas import UsuarioResponse
from src.Alertas.domain.schemas import AlertaCreate, AlertaUpdate, AlertaResponse
from src.Alertas.application.use_cases import AlertaUseCases
from src.Alertas.infrastructure.database import get_alerta_use_cases


router = APIRouter(prefix="/alertas", tags=["Alertas"])


def get_use_cases(db: Session = Depends(get_database)) -> AlertaUseCases:
    """Dependency para obtener los casos de uso de Alerta"""
    return get_alerta_use_cases(db)


@router.get(
    "/",
    response_model=List[AlertaResponse],
    summary="Listar todas las alertas",
    description="Obtiene una lista de todas las alertas ordenadas por fecha descendente (requiere autenticación)"
)
def listar_alertas(
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: AlertaUseCases = Depends(get_use_cases)
):
    """Obtener todas las alertas (requiere autenticación)"""
    return use_cases.listar_alertas()


@router.get(
    "/criticas",
    response_model=List[AlertaResponse],
    summary="Listar alertas críticas",
    description="Obtiene todas las alertas críticas (requiere autenticación)"
)
def listar_alertas_criticas(
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: AlertaUseCases = Depends(get_use_cases)
):
    """Obtener todas las alertas críticas (requiere autenticación)"""
    return use_cases.obtener_alertas_criticas()


@router.get(
    "/recientes",
    response_model=List[AlertaResponse],
    summary="Listar alertas recientes",
    description="Obtiene alertas recientes (últimas 24 horas por defecto)"
)
def listar_alertas_recientes(
    horas: int = Query(24, ge=1, le=168, description="Número de horas hacia atrás (1-168)"),
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: AlertaUseCases = Depends(get_use_cases)
):
    """Obtener alertas recientes (requiere autenticación)"""
    return use_cases.obtener_alertas_recientes(horas)


@router.get(
    "/reporte-criticas",
    summary="Reporte de alertas críticas",
    description="Genera un reporte completo de alertas críticas (requiere autenticación)"
)
def generar_reporte_criticas(
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: AlertaUseCases = Depends(get_use_cases)
):
    """Generar reporte de alertas críticas (requiere autenticación)"""
    return use_cases.generar_reporte_alertas_criticas()


@router.get(
    "/tipo/{tipo_alerta}",
    response_model=List[AlertaResponse],
    summary="Listar alertas por tipo",
    description="Obtiene todas las alertas de un tipo específico (requiere autenticación)"
)
def listar_alertas_por_tipo(
    tipo_alerta: str,
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: AlertaUseCases = Depends(get_use_cases)
):
    """Obtener todas las alertas de un tipo específico (requiere autenticación)"""
    return use_cases.obtener_alertas_por_tipo(tipo_alerta)


@router.get(
    "/lectura/{id_lectura}",
    response_model=List[AlertaResponse],
    summary="Listar alertas por lectura",
    description="Obtiene todas las alertas de una lectura específica (requiere autenticación)"
)
def listar_alertas_por_lectura(
    id_lectura: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: AlertaUseCases = Depends(get_use_cases)
):
    """Obtener todas las alertas de una lectura específica (requiere autenticación)"""
    return use_cases.obtener_alertas_por_lectura(id_lectura)


@router.get(
    "/{id_alerta}",
    response_model=AlertaResponse,
    summary="Obtener alerta por ID",
    description="Obtiene una alerta específica por su ID (requiere autenticación)"
)
def obtener_alerta(
    id_alerta: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: AlertaUseCases = Depends(get_use_cases)
):
    """Obtener una alerta por ID (requiere autenticación)"""
    return use_cases.obtener_alerta(id_alerta)


@router.post(
    "/",
    response_model=AlertaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva alerta",
    description="Crea una nueva alerta en el sistema (requiere permisos de admin o moderador)"
)
def crear_alerta(
    alerta: AlertaCreate,
    current_user: UsuarioResponse = Depends(require_admin_or_moderator()),
    use_cases: AlertaUseCases = Depends(get_use_cases)
):
    """Crear una nueva alerta (requiere admin o moderador)"""
    return use_cases.crear_alerta(alerta)


@router.put(
    "/{id_alerta}",
    response_model=AlertaResponse,
    summary="Actualizar alerta",
    description="Actualiza una alerta existente (requiere permisos de admin o moderador)"
)
def actualizar_alerta(
    id_alerta: int,
    alerta: AlertaUpdate,
    current_user: UsuarioResponse = Depends(require_admin_or_moderator()),
    use_cases: AlertaUseCases = Depends(get_use_cases)
):
    """Actualizar una alerta existente (requiere admin o moderador)"""
    return use_cases.actualizar_alerta(id_alerta, alerta)


@router.delete(
    "/{id_alerta}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar alerta",
    description="Elimina una alerta del sistema (requiere permisos de administrador)"
)
def eliminar_alerta(
    id_alerta: int,
    current_user: UsuarioResponse = Depends(require_admin()),
    use_cases: AlertaUseCases = Depends(get_use_cases)
):
    """Eliminar una alerta (requiere admin)"""
    use_cases.eliminar_alerta(id_alerta)
    return {"message": "Alerta eliminada exitosamente"}
