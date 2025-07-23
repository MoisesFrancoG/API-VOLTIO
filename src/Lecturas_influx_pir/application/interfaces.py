"""
Interfaces para el módulo de lecturas de sensores PIR
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..domain.entities import LecturaPIR


class LecturaPIRRepositoryInterface(ABC):
    """Interfaz para el repositorio de lecturas de sensores PIR"""

    @abstractmethod
    async def get_lecturas_by_time_range(
        self,
        time_range: str,
        mac_address: Optional[str] = None
    ) -> List[LecturaPIR]:
        """Obtiene lecturas PIR filtradas por rango de tiempo y opcionalmente por MAC"""
        pass
