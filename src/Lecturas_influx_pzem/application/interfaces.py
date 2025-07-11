# Contenido COMPLETO y CORREGIDO del archivo

from abc import ABC, abstractmethod
from typing import List
from src.Lecturas_influx_pzem.domain.schemas import LecturaPZEMResponse, TimeRange

class LecturaRepositoryInterface(ABC):
    """Puerto que define las operaciones de lectura para las métricas de energía."""

    @abstractmethod
    # --- CAMBIO EN LA FIRMA DEL MÉTODO ---
    def get_by_time_range(
        self, 
        time_range: TimeRange, 
        mac: str | None = None
    ) -> List[LecturaPZEMResponse]:
        pass