"""
Casos de uso para el módulo de lecturas de sensores de luz
"""

from typing import List, Optional
from .interfaces import LecturaLightRepositoryInterface
from ..domain.entities import LecturaLight
from ..domain.schemas import TimeRange


class GetLecturasLightUseCase:
    """Caso de uso para obtener lecturas de sensores de luz por rango de tiempo"""

    def __init__(self, repository: LecturaLightRepositoryInterface):
        self._repository = repository

    async def execute(
        self,
        time_range: TimeRange,
        mac_address: Optional[str] = None
    ) -> List[LecturaLight]:
        """
        Obtiene lecturas de luz filtradas por rango de tiempo y opcionalmente por MAC

        Args:
            time_range: Rango de tiempo para filtrar las lecturas
            mac_address: Dirección MAC opcional para filtrar por sensor específico

        Returns:
            Lista de lecturas de sensores de luz

        Raises:
            ValueError: Si el time_range no es válido
            Exception: Si hay error en la consulta a InfluxDB
        """
        try:
            # Validar que el time_range sea válido
            if time_range not in TimeRange:
                raise ValueError(f"Rango de tiempo inválido: {time_range}")

            # Obtener lecturas desde el repositorio
            lecturas = await self._repository.get_lecturas_by_time_range(
                time_range=time_range.value,
                mac_address=mac_address
            )

            return lecturas

        except ValueError:
            raise
        except Exception as e:
            raise Exception(
                f"Error al obtener lecturas de sensores de luz: {str(e)}")
