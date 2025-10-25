from typing import List
from src.ComandosIR.domain.schemas import DeviceCommandCreate, DeviceCommandUpdate, DeviceCommandResponse
from src.ComandosIR.application.interfaces import DeviceCommandRepositoryInterface


class DeviceCommandUseCases:
    """Use cases for the DeviceCommand entity"""

    def __init__(self, repository: DeviceCommandRepositoryInterface):
        self.repository = repository

    def list_device_commands(self) -> List[DeviceCommandResponse]:
        """List all device commands"""
        return self.repository.get_all()

    def get_device_command(self, id: int) -> DeviceCommandResponse:
        """Get a device command by ID"""
        return self.repository.get_by_id(id)

    def get_commands_by_device(self, device_id: int) -> List[DeviceCommandResponse]:
        """Get all device commands for a specific device"""
        return self.repository.get_by_device(device_id)

    def create_device_command(self, device_command: DeviceCommandCreate) -> DeviceCommandResponse:
        """Create a new device command"""
        return self.repository.create(device_command)

    def update_device_command(self, id: int, device_command: DeviceCommandUpdate) -> DeviceCommandResponse:
        """Update an existing device command"""
        return self.repository.update(id, device_command)

    def delete_device_command(self, id: int) -> None:
        """Delete a device command"""
        self.repository.delete(id)
