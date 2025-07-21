from typing import List
from src.Ubicaciones.domain.schemas import LocationCreate, LocationUpdate, LocationResponse
from src.Ubicaciones.application.interfaces import LocationRepositoryInterface


class LocationUseCases:
    """Casos de uso para la entidad Location"""

    def __init__(self, repository: LocationRepositoryInterface):
        self.repository = repository

    def list_locations(self) -> List[LocationResponse]:
        return self.repository.get_all()

    def get_location(self, location_id: int) -> LocationResponse:
        return self.repository.get_by_id(location_id)

    def create_location(self, location: LocationCreate) -> LocationResponse:
        return self.repository.create(location)

    def update_location(self, location_id: int, location: LocationUpdate) -> LocationResponse:
        return self.repository.update(location_id, location)

    def delete_location(self, location_id: int) -> None:
        self.repository.delete(location_id)
