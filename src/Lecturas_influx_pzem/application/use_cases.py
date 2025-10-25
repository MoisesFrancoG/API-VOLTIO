# Contenido COMPLETO y CORREGIDO del archivo

from typing import List
from src.Lecturas_influx_pzem.application.interfaces import LecturaRepositoryInterface
from src.Lecturas_influx_pzem.domain.schemas import LecturaPZEMResponse, TimeRange


class LecturaUseCases:
    def __init__(self, repository: LecturaRepositoryInterface):
        self.repository = repository

    # --- CAMBIO EN LA FIRMA DEL MÉTODO ---
    def obtener_lecturas_por_rango(
        self,
        time_range: TimeRange,
        mac: str | None = None,
        device_id: str | None = None
    ) -> List[LecturaPZEMResponse]:
        """Obtiene lecturas filtradas por un rango de tiempo y opcionalmente por dirección MAC o deviceId."""

        # --- Y CAMBIO EN LA LLAMADA AL REPOSITORIO ---
        return self.repository.get_by_time_range(time_range, mac, device_id)
