"""
Interfaces para el módulo de lecturas de sensores de luz
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..domain.entities import LecturaLight


class LecturaLightRepositoryInterface(ABC):
    """Interfaz para el repositorio de lecturas de sensores de luz"""

    @abstractmethod
    async def get_lecturas_by_time_range(
        self,
        time_range: str,
        mac_address: Optional[str] = None
    ) -> List[LecturaLight]:
        """Obtiene lecturas de luz filtradas por rango de tiempo y opcionalmente por MAC"""
        pass
