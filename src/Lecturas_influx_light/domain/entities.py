"""
Entidades del dominio para lecturas de sensores de luz
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LecturaLight:
    """Entidad que representa una lectura del sensor de luz"""
    mac: str
    light_level: float
    timestamp: datetime

    def __post_init__(self):
        """Validaciones después de la inicialización"""
        if not self.mac:
            raise ValueError("MAC address es requerida")
        if self.light_level is None:
            raise ValueError("Nivel de luz es requerido")
        if self.light_level < 0:
            raise ValueError("Nivel de luz no puede ser negativo")
