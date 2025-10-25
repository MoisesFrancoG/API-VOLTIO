"""
Database setup and dependency injection for Notification module
"""

from sqlalchemy.orm import Session
from src.Notifications.application.use_cases import NotificationUseCases
from src.Notifications.infrastructure.repositories import NotificationRepository


def get_notification_use_cases(db: Session) -> NotificationUseCases:
    """
    Dependency injection para los casos de uso de Notification
    """
    repository = NotificationRepository(db)
    return NotificationUseCases(repository)
