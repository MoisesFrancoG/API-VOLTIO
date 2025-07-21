# Contenido COMPLETO y CORREGIDO del archivo

from typing import List
from fastapi import APIRouter, Depends, Query

from src.core.auth_middleware import get_current_user
from src.Usuarios.domain.schemas import UserResponse
from src.Lecturas_influx_pzem.domain.schemas import LecturaPZEMResponse, TimeRange
from src.Lecturas_influx_pzem.application.use_cases import LecturaUseCases
from src.Lecturas_influx_pzem.infrastructure.database import get_lectura_use_cases

router = APIRouter(prefix="/lecturas-pzem", tags=["Lecturas PZEM"])


@router.get(
    "/{time_range}",
    response_model=List[LecturaPZEMResponse],
    summary="Obtener lecturas por rango de tiempo",
    description="Obtiene las métricas de energía de los sensores PZEM para un rango de tiempo específico (requiere autenticación)."
)
def obtener_lecturas(
    time_range: TimeRange,
    current_user: UserResponse = Depends(get_current_user),
    mac: str | None = Query(
        None, description="Filtrar por la dirección MAC del dispositivo"),
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """
    Endpoint para obtener lecturas del sensor PZEM.
    Requiere autenticación JWT - cualquier usuario autenticado puede acceder.
    """
    # El usuario autenticado puede acceder a las lecturas
    return use_cases.obtener_lecturas_por_rango(time_range, mac)
