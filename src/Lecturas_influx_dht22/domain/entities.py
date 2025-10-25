"""
Entidades del dominio para lecturas DHT22
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LecturaDHT22:
    """Entidad que representa una lectura del sensor DHT22"""
    mac: str
    temperature: float
    humidity: float
    timestamp: datetime

    def __post_init__(self):
        """Validaciones después de la inicialización"""
        if not self.mac:
            raise ValueError("MAC address es requerida")
        if self.temperature is None or self.humidity is None:
            raise ValueError("Temperatura y humedad son requeridas")
