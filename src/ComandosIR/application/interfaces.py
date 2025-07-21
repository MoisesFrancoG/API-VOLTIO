from abc import ABC, abstractmethod
from typing import List
from src.ComandosIR.domain.schemas import DeviceCommandCreate, DeviceCommandUpdate, DeviceCommandResponse


class DeviceCommandRepositoryInterface(ABC):
    """Port that defines what operations a repository must implement"""

    @abstractmethod
    def get_all(self) -> List[DeviceCommandResponse]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> DeviceCommandResponse:
        pass

    @abstractmethod
    def get_by_device(self, device_id: int) -> List[DeviceCommandResponse]:
        pass

    @abstractmethod
    def create(self, device_command: DeviceCommandCreate) -> DeviceCommandResponse:
        pass

    @abstractmethod
    def update(self, id: int, device_command: DeviceCommandUpdate) -> DeviceCommandResponse:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
