from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

# Enum para los rangos de tiempo válidos
class TimeRange(str, Enum):
    minute = "1m"
    hour = "1h"
    day = "1d"
    week = "1w"
    month = "1mo" # 'mo' es la abreviatura de Flux para mes
    year = "1y"

# Esquema para la respuesta de un único punto de datos
class LecturaPZEMResponse(BaseModel):
    time: datetime = Field(..., alias="_time")
    deviceId: str | None = None  # Hacer opcional
    mac: str
    voltage: float | None = None
    current: float | None = None
    power: float | None = None
    energy: float | None = None
    frequency: float | None = None
    powerFactor: float | None = None

    class Config:
        from_attributes = True
        populate_by_name = True # Permite usar alias como '_time'