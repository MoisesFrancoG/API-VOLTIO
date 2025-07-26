"""
Interfaces (ports) for the Devices module
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..domain.entities import Device
from ..domain.schemas import DeviceCreate, DeviceUpdate


class DeviceRepository(ABC):
    """Abstract interface for the Device repository"""

    @abstractmethod
    def create_device(self, device) -> Device:
        """Creates a new device"""
        pass

    @abstractmethod
    def get_device(self, device_id: int) -> Optional[Device]:
        """Gets a device by its ID"""
        pass

    @abstractmethod
    def get_all_devices(self) -> List[Device]:
        """Gets all devices"""
        pass

    @abstractmethod
    def get_active_devices(self) -> List[Device]:
        """Gets only active devices"""
        pass

    @abstractmethod
    def get_devices_by_type(self, device_type_id: int) -> List[Device]:
        """Gets devices by type"""
        pass

    @abstractmethod
    def get_devices_by_user(self, user_id: int) -> List[Device]:
        """Gets devices by user"""
        pass

    @abstractmethod
    def search_devices_by_name(self, name: str) -> List[Device]:
        """Searches devices by name (partial search)"""
        pass

    @abstractmethod
    def update_device(self, device_id: int, device: DeviceUpdate) -> Optional[Device]:
        """Updates an existing device"""
        pass

    @abstractmethod
    def change_device_status(self, device_id: int, active: bool) -> Optional[Device]:
        """Changes only the active/inactive status of the device"""
        pass

    @abstractmethod
    def delete_device(self, device_id: int) -> bool:
        """Deletes a device"""
        pass

    @abstractmethod
    def count_devices_by_type(self, device_type_id: int) -> int:
        """Counts devices by type"""
        pass

    @abstractmethod
    def count_devices_by_user(self, user_id: int) -> int:
        """Counts devices by user"""
        pass

    @abstractmethod
    def exists_device_with_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Checks if a device with the given name exists"""
        pass

    @abstractmethod
    def exists_device_with_mac(self, mac_address: str, exclude_id: Optional[int] = None) -> bool:
        """Checks if a device with the given MAC address exists"""
        pass

    @abstractmethod
    def get_by_mac_address(self, mac_address: str) -> Optional[Device]:
        """Gets a device by its MAC address"""
        pass

    @abstractmethod
    def get_device_with_type_by_mac(self, mac_address: str) -> Optional[dict]:
        """Gets a device with type information by MAC address"""
        pass
