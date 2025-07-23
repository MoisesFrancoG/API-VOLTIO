"""
Rutas de la API para lecturas de sensores de luz
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional

from ..application.use_cases import GetLecturasLightUseCase
from ..domain.schemas import TimeRange, LecturasListResponse, LecturaLightResponse
from ..infrastructure.repositories import LecturaLightRepository
from ...core.auth_middleware import get_current_user
from ...Usuarios.domain.schemas import UserResponse


router = APIRouter(prefix="/light", tags=["Light Sensors"])


def get_use_case() -> GetLecturasLightUseCase:
    """Inyección de dependencias para el caso de uso"""
    repository = LecturaLightRepository()
    return GetLecturasLightUseCase(repository)


@router.get("/current", response_model=LecturasListResponse)
async def get_current_light(
    mac: Optional[str] = Query(
        None, description="Filtrar por dirección MAC específica"),
    use_case: GetLecturasLightUseCase = Depends(get_use_case),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Obtiene los niveles de luz actuales

    **Parámetros:**
    - **mac**: Dirección MAC del sensor (opcional)

    **Respuesta:**
    - Últimas lecturas de nivel de luz
    """
    try:
        # Obtener último minuto de datos
        lecturas = await use_case.execute(
            time_range=TimeRange.ONE_MINUTE,
            mac_address=mac
        )

        # Convertir entidades a esquemas de respuesta
        lecturas_response = [
            LecturaLightResponse(
                mac=lectura.mac,
                light_level=lectura.light_level,
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


@router.get("/history/{time_range}", response_model=LecturasListResponse)
async def get_light_history(
    time_range: TimeRange,
    mac: Optional[str] = Query(
        None, description="Filtrar por dirección MAC específica"),
    use_case: GetLecturasLightUseCase = Depends(get_use_case),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Obtiene histórico de niveles de luz

    **Parámetros:**
    - **time_range**: Rango de tiempo (1m, 1h, 1d, 1w, 1mo, 1y)
    - **mac**: Dirección MAC del sensor (opcional)

    **Respuesta:**
    - Histórico de lecturas de nivel de luz
    """
    try:
        # Ejecutar caso de uso
        lecturas = await use_case.execute(
            time_range=time_range,
            mac_address=mac
        )

        # Convertir entidades a esquemas de respuesta
        lecturas_response = [
            LecturaLightResponse(
                mac=lectura.mac,
                light_level=lectura.light_level,
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
