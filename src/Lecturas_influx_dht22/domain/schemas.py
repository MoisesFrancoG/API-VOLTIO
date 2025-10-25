"""
Esquemas de validación y transferencia de datos para lecturas DHT22 (Pydantic)
"""

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List


class TimeRange(str, Enum):
    """Rangos de tiempo disponibles para consultas"""
    ONE_MINUTE = "1m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1mo"
    ONE_YEAR = "1y"


class LecturaDHT22Response(BaseModel):
    """Esquema de respuesta para lecturas DHT22"""
    mac: str = Field(..., description="Dirección MAC del sensor")
    temperature: float = Field(...,
                               description="Temperatura en grados Celsius")
    humidity: float = Field(..., description="Humedad relativa en porcentaje")
    timestamp: datetime = Field(..., description="Momento de la lectura")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "mac": "AA:BB:CC:DD:EE:FF",
                "temperature": 23.5,
                "humidity": 65.2,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class LecturasListResponse(BaseModel):
    """Esquema de respuesta para lista de lecturas DHT22"""
    lecturas: List[LecturaDHT22Response] = Field(
        ..., description="Lista de lecturas DHT22")
    total: int = Field(..., description="Total de lecturas encontradas")
    time_range: str = Field(..., description="Rango de tiempo consultado")

    class Config:
        from_attributes = True
