"""
Dependency configuration specific to the DeviceCommand module
"""

from sqlalchemy.orm import Session
from src.core.db import get_database
from src.ComandosIR.application.use_cases import DeviceCommandUseCases
from src.ComandosIR.infrastructure.repositories import SqlAlchemyDeviceCommandRepository


def get_device_command_repository(db: Session) -> SqlAlchemyDeviceCommandRepository:
    """Factory to create DeviceCommand repository instance"""
    return SqlAlchemyDeviceCommandRepository(db)


def get_device_command_use_cases(db: Session) -> DeviceCommandUseCases:
    """Factory to create DeviceCommand use cases instance"""
    repository = get_device_command_repository(db)
    return DeviceCommandUseCases(repository)
