from typing import List
from src.Ubicaciones.domain.schemas import UbicacionCreate, UbicacionUpdate, UbicacionResponse
from src.Ubicaciones.application.interfaces import UbicacionRepositoryInterface


class UbicacionUseCases:
    """Casos de uso para la entidad Ubicacion"""

    def __init__(self, repository: UbicacionRepositoryInterface):
        self.repository = repository

    def listar_ubicaciones(self) -> List[UbicacionResponse]:
        return self.repository.get_all()

    def obtener_ubicacion(self, id_ubicacion: int) -> UbicacionResponse:
        return self.repository.get_by_id(id_ubicacion)

    def crear_ubicacion(self, ubicacion: UbicacionCreate) -> UbicacionResponse:
        return self.repository.create(ubicacion)

    def actualizar_ubicacion(self, id_ubicacion: int, ubicacion: UbicacionUpdate) -> UbicacionResponse:
        return self.repository.update(id_ubicacion, ubicacion)

    def eliminar_ubicacion(self, id_ubicacion: int) -> None:
        self.repository.delete(id_ubicacion)
