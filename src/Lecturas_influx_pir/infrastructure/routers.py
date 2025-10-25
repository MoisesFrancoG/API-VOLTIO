"""
Rutas de la API para lecturas de sensores PIR
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional

from ..application.use_cases import GetLecturasPIRUseCase
from ..domain.schemas import TimeRange, LecturasListResponse, LecturaPIRResponse
from ..infrastructure.repositories import LecturaPIRRepository
from ...core.auth_middleware import get_current_user
from ...Usuarios.domain.schemas import UserResponse


router = APIRouter(prefix="/motion", tags=["Motion Sensors - PIR"])


def get_use_case() -> GetLecturasPIRUseCase:
    """Inyección de dependencias para el caso de uso"""
    repository = LecturaPIRRepository()
    return GetLecturasPIRUseCase(repository)


@router.get("/current", response_model=LecturasListResponse)
async def get_current_motion(
    mac: Optional[str] = Query(
        None, description="Filtrar por dirección MAC específica"),
    use_case: GetLecturasPIRUseCase = Depends(get_use_case),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Obtiene el estado actual de movimiento de los sensores PIR

    **Parámetros:**
    - **mac**: Dirección MAC del sensor (opcional)

    **Respuesta:**
    - Estado actual de detección de movimiento
    """
    try:
        # Obtener último minuto de datos
        lecturas = await use_case.execute(
            time_range=TimeRange.ONE_MINUTE,
            mac_address=mac
        )

        # Convertir entidades a esquemas de respuesta
        lecturas_response = [
            LecturaPIRResponse(
                mac=lectura.mac,
                motion_detected=lectura.motion_detected,
                timestamp=lectura.timestamp
            )
            for lectura in lecturas
        ]

        # Preparar respuesta final
        response = LecturasListResponse(
            lecturas=lecturas_response,
            total=len(lecturas_response),
            time_range="current"
        )

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/events/{time_range}", response_model=LecturasListResponse)
async def get_motion_events(
    time_range: TimeRange,
    mac: Optional[str] = Query(
        None, description="Filtrar por dirección MAC específica"),
    use_case: GetLecturasPIRUseCase = Depends(get_use_case),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Obtiene eventos de movimiento por rango de tiempo

    **Parámetros:**
    - **time_range**: Rango de tiempo (1m, 1h, 1d, 1w, 1mo, 1y)
    - **mac**: Dirección MAC del sensor (opcional)

    **Respuesta:**
    - Lista de eventos de movimiento detectados
    """
    try:
        # Ejecutar caso de uso
        lecturas = await use_case.execute(
            time_range=time_range,
            mac_address=mac
        )

        # Convertir entidades a esquemas de respuesta
        lecturas_response = [
            LecturaPIRResponse(
                mac=lectura.mac,
                motion_detected=lectura.motion_detected,
                timestamp=lectura.timestamp
            )
            for lectura in lecturas
        ]

        # Preparar respuesta final
        response = LecturasListResponse(
            lecturas=lecturas_response,
            total=len(lecturas_response),
            time_range=time_range.value
        )

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}")
