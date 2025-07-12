from abc import ABC, abstractmethod
from typing import List
from src.Ubicaciones.domain.schemas import UbicacionCreate, UbicacionUpdate, UbicacionResponse


class UbicacionRepositoryInterface(ABC):
    """Puerto que define qué operaciones debe implementar un repositorio"""

    @abstractmethod
    def get_all(self) -> List[UbicacionResponse]:
        pass

    @abstractmethod
    def get_by_id(self, id_ubicacion: int) -> UbicacionResponse:
        pass

    @abstractmethod
    def create(self, ubicacion: UbicacionCreate) -> UbicacionResponse:
        pass

    @abstractmethod
    def update(self, id_ubicacion: int, ubicacion: UbicacionUpdate) -> UbicacionResponse:
        pass

    @abstractmethod
    def delete(self, id_ubicacion: int) -> None:
        pass
