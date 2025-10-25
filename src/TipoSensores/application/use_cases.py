from typing import List
from src.TipoSensores.domain.schemas import DeviceTypeCreate, DeviceTypeUpdate, DeviceTypeResponse
from src.TipoSensores.application.interfaces import DeviceTypeRepositoryInterface


class DeviceTypeUseCases:
    """Use cases for the DeviceType entity"""

    def __init__(self, repository: DeviceTypeRepositoryInterface):
        self.repository = repository

    def list_device_types(self) -> List[DeviceTypeResponse]:
        return self.repository.get_all()

    def get_device_type(self, device_type_id: int) -> DeviceTypeResponse:
        return self.repository.get_by_id(device_type_id)

    def create_device_type(self, device_type: DeviceTypeCreate) -> DeviceTypeResponse:
        return self.repository.create(device_type)

    def update_device_type(self, device_type_id: int, device_type: DeviceTypeUpdate) -> DeviceTypeResponse:
        return self.repository.update(device_type_id, device_type)

    def delete_device_type(self, device_type_id: int) -> None:
        self.repository.delete(device_type_id)
