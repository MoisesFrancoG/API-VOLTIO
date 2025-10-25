"""
Domain entities for Notification
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Notification:
    """Entidad de dominio para Notificación"""
    id: Optional[int]
    user_id: int
    device_id: Optional[int]
    message: str
    is_read: bool
    created_at: Optional[datetime]

    def mark_as_read(self) -> None:
        """Marcar la notificación como leída"""
        self.is_read = True

    def mark_as_unread(self) -> None:
        """Marcar la notificación como no leída"""
        self.is_read = False

    def is_device_related(self) -> bool:
        """Verificar si la notificación está relacionada con un dispositivo"""
        return self.device_id is not None
