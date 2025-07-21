"""
Domain entities for Devices module
"""

from typing import Optional
from datetime import datetime


class Device:
    """Device domain entity"""

    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        device_type_id: int = 0,
        location_id: int = 0,
        user_id: int = 0,
        is_active: bool = True,
        mac_address: Optional[str] = None,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.device_type_id = device_type_id
        self.location_id = location_id
        self.user_id = user_id
        self.is_active = is_active
        self.mac_address = mac_address
        self.description = description
        self.created_at = created_at

    def activate(self) -> None:
        """Activate the device"""
        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate the device"""
        self.is_active = False

    def is_device_active(self) -> bool:
        """Check if device is active"""
        return self.is_active

    def update_device_info(self, name: str = None, description: str = None) -> None:
        """Update device information"""
        if name:
            self.name = name
        if description:
            self.description = description

    def assign_to_location(self, location_id: int) -> None:
        """Assign device to a location"""
        self.location_id = location_id

    def assign_to_user(self, user_id: int) -> None:
        """Assign device to a user"""
        self.user_id = user_id

    def can_be_deleted(self) -> bool:
        """Check if device can be safely deleted"""
        # Business logic: only inactive devices can be deleted
        return not self.is_active

    def __repr__(self):
        return f"<Device(id={self.id}, name='{self.name}', is_active={self.is_active})>"

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"
