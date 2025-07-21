"""
Interfaces for Notification repository
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.Notifications.domain.entities import Notification
from src.Notifications.domain.schemas import NotificationCreate, NotificationUpdate


class NotificationRepositoryInterface(ABC):
    """Interface para el repositorio de notificaciones"""

    @abstractmethod
    def create(self, notification: NotificationCreate) -> Notification:
        """Crear una nueva notificación"""
        pass

    @abstractmethod
    def get_by_id(self, notification_id: int, user_id: int) -> Optional[Notification]:
        """Obtener una notificación por ID, verificando que pertenezca al usuario"""
        pass

    @abstractmethod
    def get_by_user(
        self,
        user_id: int,
        is_read: Optional[bool] = None,
        device_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Notification]:
        """Obtener notificaciones de un usuario con filtros opcionales"""
        pass

    @abstractmethod
    def update(self, notification_id: int, user_id: int, notification_update: NotificationUpdate) -> Optional[Notification]:
        """Actualizar una notificación"""
        pass

    @abstractmethod
    def delete(self, notification_id: int, user_id: int) -> bool:
        """Eliminar una notificación"""
        pass

    @abstractmethod
    def mark_as_read(self, notification_id: int, user_id: int) -> Optional[Notification]:
        """Marcar una notificación como leída"""
        pass

    @abstractmethod
    def mark_all_as_read(self, user_id: int) -> int:
        """Marcar todas las notificaciones de un usuario como leídas"""
        pass

    @abstractmethod
    def count_unread(self, user_id: int) -> int:
        """Contar notificaciones no leídas de un usuario"""
        pass

    @abstractmethod
    def delete_old_read_notifications(self, user_id: int, days_old: int = 30) -> int:
        """Eliminar notificaciones leídas antiguas"""
        pass
