"""
Dependency configuration specific to the DeviceTypes module
"""

from sqlalchemy.orm import Session
from src.core.db import get_database
from src.TipoSensores.application.use_cases import DeviceTypeUseCases
from src.TipoSensores.infrastructure.repositories import SqlAlchemyDeviceTypeRepository


def get_device_type_repository(db: Session) -> SqlAlchemyDeviceTypeRepository:
    """Factory to create DeviceType repository instance"""
    return SqlAlchemyDeviceTypeRepository(db)


def get_device_type_use_cases(db: Session) -> DeviceTypeUseCases:
    """Factory to create DeviceType use cases instance"""
    repository = get_device_type_repository(db)
    return DeviceTypeUseCases(repository)
