"""
Interfaces para el módulo de lecturas DHT22
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..domain.entities import LecturaDHT22


class LecturaDHT22RepositoryInterface(ABC):
    """Interfaz para el repositorio de lecturas DHT22"""

    @abstractmethod
    async def get_lecturas_by_time_range(
        self,
        time_range: str,
        mac_address: Optional[str] = None
    ) -> List[LecturaDHT22]:
        """Obtiene lecturas DHT22 filtradas por rango de tiempo y opcionalmente por MAC"""
        pass
