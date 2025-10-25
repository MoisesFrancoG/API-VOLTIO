"""
Rutas de la API para lecturas DHT22
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional

from ..application.use_cases import GetLecturasDHT22UseCase
from ..domain.schemas import TimeRange, LecturasListResponse, LecturaDHT22Response
from ..infrastructure.repositories import LecturaDHT22Repository
from ...core.auth_middleware import get_current_user
from ...Usuarios.domain.schemas import UserResponse


router = APIRouter(prefix="/environment", tags=["Environment - DHT22 Sensors"])


def get_use_case() -> GetLecturasDHT22UseCase:
    """Inyección de dependencias para el caso de uso"""
    repository = LecturaDHT22Repository()
    return GetLecturasDHT22UseCase(repository)


@router.get("/current", response_model=LecturasListResponse)
async def get_current_environment(
    mac: Optional[str] = Query(
        None, description="Filtrar por dirección MAC específica"),
    use_case: GetLecturasDHT22UseCase = Depends(get_use_case),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Obtiene las últimas lecturas ambientales (DHT22)

    **Parámetros:**
    - **mac**: Dirección MAC del sensor (opcional)

    **Respuesta:**
    - Últimas lecturas de temperatura y humedad
    """
    try:
        # Obtener último minuto de datos
        lecturas = await use_case.execute(
            time_range=TimeRange.ONE_MINUTE,
            mac_address=mac
        )

        # Convertir entidades a esquemas de respuesta
        lecturas_response = [
            LecturaDHT22Response(
                mac=lectura.mac,
                temperature=lectura.temperature,
                humidity=lectura.humidity,
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
async def get_environment_history(
    time_range: TimeRange,
    mac: Optional[str] = Query(
        None, description="Filtrar por dirección MAC específica"),
    use_case: GetLecturasDHT22UseCase = Depends(get_use_case),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Obtiene histórico de lecturas ambientales (DHT22)

    **Parámetros:**
    - **time_range**: Rango de tiempo (1m, 1h, 1d, 1w, 1mo, 1y)
    - **mac**: Dirección MAC del sensor (opcional)

    **Respuesta:**
    - Histórico de lecturas de temperatura y humedad
    """
    try:
        # Ejecutar caso de uso
        lecturas = await use_case.execute(
            time_range=time_range,
            mac_address=mac
        )

        # Convertir entidades a esquemas de respuesta
        lecturas_response = [
            LecturaDHT22Response(
                mac=lectura.mac,
                temperature=lectura.temperature,
                humidity=lectura.humidity,
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
