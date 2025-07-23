# Contenido COMPLETO y CORREGIDO del archivo

from typing import List
from fastapi import APIRouter, Depends, Query

from src.core.auth_middleware import get_current_user
from src.Usuarios.domain.schemas import UserResponse
from src.Lecturas_influx_pzem.domain.schemas import LecturaPZEMResponse, TimeRange
from src.Lecturas_influx_pzem.application.use_cases import LecturaUseCases
from src.Lecturas_influx_pzem.infrastructure.database import get_lectura_use_cases

router = APIRouter(prefix="/energy", tags=["Energy Meters - PZEM"])


@router.get("/current", response_model=List[LecturaPZEMResponse])
def get_current_energy(
    current_user: UserResponse = Depends(get_current_user),
    mac: str | None = Query(
        None, description="Filtrar por la dirección MAC del dispositivo"),
    device_id: str | None = Query(
        None, description="Filtrar por el ID del dispositivo PZEM", alias="deviceId"),
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """
    Obtiene las lecturas de energía actuales (último minuto)
    Requiere autenticación JWT - cualquier usuario autenticado puede acceder.
    """
    # El usuario autenticado puede acceder a las lecturas actuales
    return use_cases.obtener_lecturas_por_rango(TimeRange.minute, mac, device_id)


@router.get("/history/{time_range}", response_model=List[LecturaPZEMResponse])
def get_energy_history(
    time_range: TimeRange,
    current_user: UserResponse = Depends(get_current_user),
    mac: str | None = Query(
        None, description="Filtrar por la dirección MAC del dispositivo"),
    device_id: str | None = Query(
        None, description="Filtrar por el ID del dispositivo PZEM", alias="deviceId"),
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """
    Obtiene el histórico de lecturas de energía por rango de tiempo
    Requiere autenticación JWT - cualquier usuario autenticado puede acceder.
    """
    # El usuario autenticado puede acceder a las lecturas
    return use_cases.obtener_lecturas_por_rango(time_range, mac, device_id)


@router.get("/devices", response_model=List[str])
def get_energy_devices(
    current_user: UserResponse = Depends(get_current_user),
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """
    Obtiene la lista de dispositivos PZEM disponibles
    Requiere autenticación JWT - cualquier usuario autenticado puede acceder.
    """
    # Por ahora retornamos una lista simple - esto puede mejorarse
    # consultando InfluxDB para obtener todos los MACs únicos
    return ["PZEM-001", "PZEM-002", "PZEM-003"]
