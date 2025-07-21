from abc import ABC, abstractmethod
from typing import List
from src.Ubicaciones.domain.schemas import LocationCreate, LocationUpdate, LocationResponse


class LocationRepositoryInterface(ABC):
    """Puerto que define qué operaciones debe implementar un repositorio"""

    @abstractmethod
    def get_all(self) -> List[LocationResponse]:
        pass

    @abstractmethod
    def get_by_id(self, location_id: int) -> LocationResponse:
        pass

    @abstractmethod
    def create(self, location: LocationCreate) -> LocationResponse:
        pass

    @abstractmethod
    def update(self, location_id: int, location: LocationUpdate) -> LocationResponse:
        pass

    @abstractmethod
    def delete(self, location_id: int) -> None:
        pass
