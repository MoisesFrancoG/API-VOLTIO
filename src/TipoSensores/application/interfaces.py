from abc import ABC, abstractmethod
from typing import List
from src.TipoSensores.domain.schemas import DeviceTypeCreate, DeviceTypeUpdate, DeviceTypeResponse


class DeviceTypeRepositoryInterface(ABC):
    """Port that defines what operations a repository must implement"""

    @abstractmethod
    def get_all(self) -> List[DeviceTypeResponse]:
        pass

    @abstractmethod
    def get_by_id(self, device_type_id: int) -> DeviceTypeResponse:
        pass

    @abstractmethod
    def create(self, device_type: DeviceTypeCreate) -> DeviceTypeResponse:
        pass

    @abstractmethod
    def update(self, device_type_id: int, device_type: DeviceTypeUpdate) -> DeviceTypeResponse:
        pass

    @abstractmethod
    def delete(self, device_type_id: int) -> None:
        pass
