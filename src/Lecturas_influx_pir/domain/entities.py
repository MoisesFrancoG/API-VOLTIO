"""
Entidades del dominio para lecturas de sensores PIR (movimiento)
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LecturaPIR:
    """Entidad que representa una lectura del sensor PIR"""
    mac: str
    motion_detected: bool
    timestamp: datetime

    def __post_init__(self):
        """Validaciones después de la inicialización"""
        if not self.mac:
            raise ValueError("MAC address es requerida")
        if self.motion_detected is None:
            raise ValueError("Estado de detección de movimiento es requerido")
