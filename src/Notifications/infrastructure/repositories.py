"""
SQLAlchemy repository implementation for Notification
"""

from datetime import datetime, timedelta
from typing import List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from src.Notifications.application.interfaces import NotificationRepositoryInterface
from src.Notifications.domain.entities import Notification
from src.Notifications.domain.schemas import NotificationCreate, NotificationUpdate, NotificationCreateInternal
from src.Notifications.infrastructure.models import NotificationModel


class NotificationRepository(NotificationRepositoryInterface):
    """Implementación del repositorio de notificaciones usando SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def _model_to_entity(self, model: NotificationModel) -> Notification:
        """Convertir modelo de SQLAlchemy a entidad de dominio"""
        return Notification(
            id=model.id,
            user_id=model.user_id,
            device_id=model.device_id,
            message=model.message,
            is_read=model.is_read,
            created_at=model.created_at
        )

    def create(self, notification: Union[NotificationCreate, NotificationCreateInternal]) -> Notification:
        """Crear una nueva notificación"""
        # Para NotificationCreateInternal, user_id viene en el objeto
        # Para NotificationCreate, user_id debe ser inyectado externamente
        user_id = getattr(notification, 'user_id', None)

        db_notification = NotificationModel(
            user_id=user_id,
            device_id=notification.device_id,
            message=notification.message,
            is_read=notification.is_read
        )

        self.db.add(db_notification)
        self.db.commit()
        self.db.refresh(db_notification)

        return self._model_to_entity(db_notification)

    def get_by_id(self, notification_id: int, user_id: int) -> Optional[Notification]:
        """Obtener una notificación por ID, verificando que pertenezca al usuario"""
        db_notification = self.db.query(NotificationModel).filter(
            and_(
                NotificationModel.id == notification_id,
                NotificationModel.user_id == user_id
            )
        ).first()

        if db_notification:
            return self._model_to_entity(db_notification)
        return None

    def get_by_user(
        self,
        user_id: int,
        is_read: Optional[bool] = None,
        device_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Notification]:
        """Obtener notificaciones de un usuario con filtros opcionales"""
        query = self.db.query(NotificationModel).filter(
            NotificationModel.user_id == user_id
        )

        # Aplicar filtros opcionales
        if is_read is not None:
            query = query.filter(NotificationModel.is_read == is_read)

        if device_id is not None:
            query = query.filter(NotificationModel.device_id == device_id)

        # Ordenar por fecha de creación (más recientes primero)
        query = query.order_by(desc(NotificationModel.created_at))

        # Aplicar paginación
        db_notifications = query.offset(offset).limit(limit).all()

        return [self._model_to_entity(notification) for notification in db_notifications]

    def update(self, notification_id: int, user_id: int, notification_update: NotificationUpdate) -> Optional[Notification]:
        """Actualizar una notificación"""
        db_notification = self.db.query(NotificationModel).filter(
            and_(
                NotificationModel.id == notification_id,
                NotificationModel.user_id == user_id
            )
        ).first()

        if not db_notification:
            return None

        # Actualizar solo los campos que no son None
        update_data = notification_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_notification, field, value)

        self.db.commit()
        self.db.refresh(db_notification)

        return self._model_to_entity(db_notification)

    def delete(self, notification_id: int, user_id: int) -> bool:
        """Eliminar una notificación"""
        db_notification = self.db.query(NotificationModel).filter(
            and_(
                NotificationModel.id == notification_id,
                NotificationModel.user_id == user_id
            )
        ).first()

        if not db_notification:
            return False

        self.db.delete(db_notification)
        self.db.commit()
        return True

    def mark_as_read(self, notification_id: int, user_id: int) -> Optional[Notification]:
        """Marcar una notificación como leída"""
        update_data = NotificationUpdate(is_read=True)
        return self.update(notification_id, user_id, update_data)

    def mark_all_as_read(self, user_id: int) -> int:
        """Marcar todas las notificaciones de un usuario como leídas"""
        updated_count = self.db.query(NotificationModel).filter(
            and_(
                NotificationModel.user_id == user_id,
                NotificationModel.is_read == False
            )
        ).update({NotificationModel.is_read: True})

        self.db.commit()
        return updated_count

    def count_unread(self, user_id: int) -> int:
        """Contar notificaciones no leídas de un usuario"""
        return self.db.query(NotificationModel).filter(
            and_(
                NotificationModel.user_id == user_id,
                NotificationModel.is_read == False
            )
        ).count()

    def delete_old_read_notifications(self, user_id: int, days_old: int = 30) -> int:
        """Eliminar notificaciones leídas antiguas"""
        cutoff_date = datetime.now() - timedelta(days=days_old)

        deleted_count = self.db.query(NotificationModel).filter(
            and_(
                NotificationModel.user_id == user_id,
                NotificationModel.is_read == True,
                NotificationModel.created_at < cutoff_date
            )
        ).delete()

        self.db.commit()
        return deleted_count
