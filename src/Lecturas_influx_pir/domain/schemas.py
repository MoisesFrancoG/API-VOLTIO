"""
Esquemas de validación y transferencia de datos para lecturas de sensores PIR (Pydantic)
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


class LecturaPIRResponse(BaseModel):
    """Esquema de respuesta para lecturas de sensores PIR"""
    mac: str = Field(..., description="Dirección MAC del sensor")
    motion_detected: bool = Field(...,
                                  description="Indica si se detectó movimiento")
    timestamp: datetime = Field(..., description="Momento de la lectura")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "mac": "AA:BB:CC:DD:EE:FF",
                "motion_detected": True,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class LecturasListResponse(BaseModel):
    """Esquema de respuesta para lista de lecturas de sensores PIR"""
    lecturas: List[LecturaPIRResponse] = Field(
        ..., description="Lista de lecturas PIR")
    total: int = Field(..., description="Total de lecturas encontradas")
    time_range: str = Field(..., description="Rango de tiempo consultado")

    class Config:
        from_attributes = True
