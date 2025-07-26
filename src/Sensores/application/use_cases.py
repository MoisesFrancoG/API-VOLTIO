"""
Use cases for the Devices module
"""

from typing import List, Optional

from .interfaces import DeviceRepository
from ..domain.entities import Device
from ..domain.schemas import DeviceCreate, DeviceUpdate, DeviceBase


class DeviceUseCases:
    def validate_ir_command_permissions(self, mac_address: str, user_id: int) -> dict:
        """
        Validates if a user can send IR commands to a device

        Args:
            mac_address: MAC address of the device
            user_id: ID of the user requesting the command

        Returns:
            dict: Validation result with device info and permissions

        Raises:
            ValueError: If validation fails
        """
        # Get device with type information
        device_info = self.repository.get_device_with_type_by_mac(mac_address)

        print(device_info)

        if not device_info:
            raise ValueError("Device not found")

        device = device_info['device']
        type_name = device_info['type_name']

        # Verify ownership
        if device.user_id != user_id:
            raise ValueError("Access denied - device not owned by user")

        # Verify device type (using ID 2 for NODO_CONTROL_IR)
        print(device.device_type_id)
        if device.device_type_id != 3:  # NODO_CONTROL_IR
            raise ValueError(
                "Operation not allowed - this command is only applicable to 'NODO_CONTROL_IR' devices"
            )

        return {
            'device': device,
            'type_name': type_name,
            'can_control_ir': True
        }
    """Use cases for Device operations"""

    def __init__(self, repository: DeviceRepository):
        self.repository = repository

    def create_device(self, device_data) -> Device:
        """Creates a new device"""
        # Validate that the name is not duplicated
        if self.repository.exists_device_with_name(device_data.name):
            raise ValueError(
                f"Device with name '{device_data.name}' already exists")

        # Validate MAC address uniqueness if provided
        if hasattr(device_data, 'mac_address') and device_data.mac_address:
            if self.repository.exists_device_with_mac(device_data.mac_address):
                raise ValueError(
                    f"Device with MAC address '{device_data.mac_address}' already exists")

        # Additional business validations
        if device_data.device_type_id <= 0:
            raise ValueError("Device type ID must be a positive number")

        if device_data.user_id <= 0:
            raise ValueError("User ID must be a positive number")

        return self.repository.create_device(device_data)

    def get_device(self, device_id: int) -> Optional[Device]:
        """Gets a device by its ID"""
        if device_id <= 0:
            raise ValueError("Device ID must be a positive number")

        return self.repository.get_device(device_id)

    def get_all_devices(self) -> List[Device]:
        """Gets all devices"""
        return self.repository.get_all_devices()

    def get_active_devices(self) -> List[Device]:
        """Gets only active devices"""
        return self.repository.get_active_devices()

    def get_devices_by_type(self, device_type_id: int) -> List[Device]:
        """Gets devices by type"""
        if device_type_id <= 0:
            raise ValueError("Device type ID must be a positive number")

        return self.repository.get_devices_by_type(device_type_id)

    # Eliminado get_devices_by_location porque location_id ya no existe

    def get_devices_by_user(self, user_id: int) -> List[Device]:
        """Gets devices by user"""
        if user_id <= 0:
            raise ValueError("User ID must be a positive number")

        return self.repository.get_devices_by_user(user_id)

    def search_devices_by_name(self, name: str) -> List[Device]:
        """Searches devices by name"""
        if not name or len(name.strip()) < 2:
            raise ValueError("Search term must have at least 2 characters")

        return self.repository.search_devices_by_name(name.strip())

    def update_device(self, device_id: int, device_data: DeviceUpdate) -> Optional[Device]:
        """Updates an existing device"""
        if device_id <= 0:
            raise ValueError("Device ID must be a positive number")

        # Validate that the device exists
        existing_device = self.repository.get_device(device_id)
        if not existing_device:
            return None

        # Validate unique name if changing
        if device_data.name and device_data.name != existing_device.name:
            if self.repository.exists_device_with_name(device_data.name, device_id):
                raise ValueError(
                    f"Another device with name '{device_data.name}' already exists")

        # Validate unique MAC address if changing
        if hasattr(device_data, 'mac_address') and device_data.mac_address:
            if hasattr(existing_device, 'mac_address') and device_data.mac_address != existing_device.mac_address:
                if self.repository.exists_device_with_mac(device_data.mac_address, device_id):
                    raise ValueError(
                        f"Another device with MAC address '{device_data.mac_address}' already exists")

        # Additional validations
        if device_data.device_type_id is not None and device_data.device_type_id <= 0:
            raise ValueError("Device type ID must be a positive number")

        if device_data.user_id is not None and device_data.user_id <= 0:
            raise ValueError("User ID must be a positive number")

        return self.repository.update_device(device_id, device_data)

    def change_device_status(self, device_id: int, active: bool) -> Optional[Device]:
        """Changes only the active/inactive status of the device"""
        if device_id <= 0:
            raise ValueError("Device ID must be a positive number")

        existing_device = self.repository.get_device(device_id)
        if not existing_device:
            return None

        if existing_device.is_active == active:
            raise ValueError(
                f"Device is already {'active' if active else 'inactive'}")

        return self.repository.change_device_status(device_id, active)

    def delete_device(self, device_id: int) -> bool:
        """Deletes a device"""
        if device_id <= 0:
            raise ValueError("Device ID must be a positive number")

        return self.repository.delete_device(device_id)

    def get_statistics_by_type(self, device_type_id: int) -> dict:
        """Gets device statistics by type"""
        if device_type_id <= 0:
            raise ValueError("Device type ID must be a positive number")

        total_devices = self.repository.count_devices_by_type(device_type_id)
        devices_of_type = self.repository.get_devices_by_type(device_type_id)
        active_devices = len([d for d in devices_of_type if d.is_active])
        inactive_devices = total_devices - active_devices

        return {
            "device_type_id": device_type_id,
            "total_devices": total_devices,
            "active_devices": active_devices,
            "inactive_devices": inactive_devices,
            "active_percentage": round((active_devices / total_devices) * 100, 2) if total_devices > 0 else 0
        }

    def get_statistics_by_location(self, location_id: int) -> dict:
        """Gets device statistics by location"""
        if location_id <= 0:
            raise ValueError("Location ID must be a positive number")

        total_devices = self.repository.count_devices_by_location(location_id)
        devices_in_location = self.repository.get_devices_by_location(
            location_id)
        active_devices = len([d for d in devices_in_location if d.is_active])
        inactive_devices = total_devices - active_devices

        return {
            "location_id": location_id,
            "total_devices": total_devices,
            "active_devices": active_devices,
            "inactive_devices": inactive_devices,
            "active_percentage": round((active_devices / total_devices) * 100, 2) if total_devices > 0 else 0
        }

    def get_statistics_by_user(self, user_id: int) -> dict:
        """Gets device statistics by user"""
        if user_id <= 0:
            raise ValueError("User ID must be a positive number")

        total_devices = self.repository.count_devices_by_user(user_id)
        user_devices = self.repository.get_devices_by_user(user_id)
        active_devices = len([d for d in user_devices if d.is_active])
        inactive_devices = total_devices - active_devices

        return {
            "user_id": user_id,
            "total_devices": total_devices,
            "active_devices": active_devices,
            "inactive_devices": inactive_devices,
            "active_percentage": round((active_devices / total_devices) * 100, 2) if total_devices > 0 else 0
        }

    def validate_device_configuration(self, device_id: int) -> dict:
        """Validates device configuration"""
        if device_id <= 0:
            raise ValueError("Device ID must be a positive number")

        device = self.repository.get_device(device_id)
        if not device:
            raise ValueError("Device not found")

        # Create domain entity for validation
        device_entity = Device(
            id=device.id,
            name=device.name,
            device_type_id=device.device_type_id,
            location_id=device.location_id,
            user_id=device.user_id,
            active=device.is_active
        )

        configuration_valid = device_entity.validate_configuration()
        can_generate_readings = device_entity.can_generate_readings()

        return {
            "device_id": device_id,
            "configuration_valid": configuration_valid,
            "can_generate_readings": can_generate_readings,
            "is_active": device_entity.is_active(),
            "validations": {
                "name_valid": len(device.name.strip()) >= 3,
                "device_type_valid": device.device_type_id > 0,
                "location_valid": device.location_id > 0,
                "user_valid": device.user_id > 0
            }
        }

    def validate_relay_command_permissions(self, mac_address: str, user_id: int) -> dict:
        """
        Validates if a user can send relay commands to a device

        Args:
            mac_address: MAC address of the device
            user_id: ID of the user requesting the command

        Returns:
            dict: Validation result with device info and permissions

        Raises:
            ValueError: If validation fails
        """
        # Get device with type information
        device_info = self.repository.get_device_with_type_by_mac(mac_address)

        if not device_info:
            raise ValueError("Device not found")

        device = device_info['device']
        type_name = device_info['type_name']

        # Verify ownership
        if device.user_id != user_id:
            raise ValueError("Access denied - device not owned by user")

        # Verify device type (using ID 1 for NODO_CONTROL_PZEM)
        # We validate by ID for better performance as requested
        if device.device_type_id != 1:  # NODO_CONTROL_PZEM
            raise ValueError(
                "Operation not allowed - this command is only applicable to 'NODO_CONTROL_PZEM' devices"
            )

        return {
            'device': device,
            'type_name': type_name,
            'can_control_relay': True
        }
