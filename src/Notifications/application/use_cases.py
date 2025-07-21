"""
Use cases for Notification management
"""

from typing import List, Optional
from src.Notifications.application.interfaces import NotificationRepositoryInterface
from src.Notifications.domain.schemas import (
    NotificationCreate, NotificationUpdate, NotificationResponse,
    NotificationFilters, NotificationMarkAsRead
)


class NotificationUseCases:
    """Casos de uso para la gestión de notificaciones"""

    def __init__(self, repository: NotificationRepositoryInterface):
        self.repository = repository

    def create_notification(self, notification: NotificationCreate) -> NotificationResponse:
        """Crear una nueva notificación"""
        created_notification = self.repository.create(notification)
        return NotificationResponse.model_validate(created_notification)

    def get_user_notifications(
        self,
        user_id: int,
        filters: Optional[NotificationFilters] = None
    ) -> List[NotificationResponse]:
        """Obtener notificaciones de un usuario con filtros"""
        if filters is None:
            filters = NotificationFilters()

        notifications = self.repository.get_by_user(
            user_id=user_id,
            is_read=filters.is_read,
            device_id=filters.device_id,
            limit=filters.limit,
            offset=filters.offset
        )

        return [NotificationResponse.model_validate(notification) for notification in notifications]

    def get_notification(self, notification_id: int, user_id: int) -> Optional[NotificationResponse]:
        """Obtener una notificación específica del usuario"""
        notification = self.repository.get_by_id(notification_id, user_id)
        if notification:
            return NotificationResponse.model_validate(notification)
        return None

    def update_notification(
        self,
        notification_id: int,
        user_id: int,
        notification_update: NotificationUpdate
    ) -> Optional[NotificationResponse]:
        """Actualizar una notificación"""
        updated_notification = self.repository.update(
            notification_id, user_id, notification_update)
        if updated_notification:
            return NotificationResponse.model_validate(updated_notification)
        return None

    def mark_as_read(self, notification_id: int, user_id: int) -> Optional[NotificationResponse]:
        """Marcar una notificación como leída"""
        updated_notification = self.repository.mark_as_read(
            notification_id, user_id)
        if updated_notification:
            return NotificationResponse.model_validate(updated_notification)
        return None

    def mark_all_as_read(self, user_id: int) -> int:
        """Marcar todas las notificaciones como leídas"""
        return self.repository.mark_all_as_read(user_id)

    def delete_notification(self, notification_id: int, user_id: int) -> bool:
        """Eliminar una notificación"""
        return self.repository.delete(notification_id, user_id)

    def get_unread_count(self, user_id: int) -> int:
        """Obtener el número de notificaciones no leídas"""
        return self.repository.count_unread(user_id)

    def clean_old_notifications(self, user_id: int, days_old: int = 30) -> int:
        """Limpiar notificaciones leídas antiguas"""
        return self.repository.delete_old_read_notifications(user_id, days_old)

    def create_device_notification(
        self,
        user_id: int,
        device_id: int,
        message: str
    ) -> NotificationResponse:
        """Crear una notificación relacionada con un dispositivo"""
        notification_data = NotificationCreate(
            user_id=user_id,
            device_id=device_id,
            message=message,
            is_read=False
        )
        return self.create_notification(notification_data)

    def create_system_notification(self, user_id: int, message: str) -> NotificationResponse:
        """Crear una notificación del sistema (sin dispositivo asociado)"""
        notification_data = NotificationCreate(
            user_id=user_id,
            device_id=None,
            message=message,
            is_read=False
        )
        return self.create_notification(notification_data)
