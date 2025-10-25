"""
Dependency configuration for the Devices module
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from ...core.db import get_database
from ..application.use_cases import DeviceUseCases
from .repositories import SQLAlchemyDeviceRepository


def get_device_repository(db: Session = Depends(get_database)) -> SQLAlchemyDeviceRepository:
    """Get Device repository instance"""
    return SQLAlchemyDeviceRepository(db)


def get_device_use_cases(repository: SQLAlchemyDeviceRepository = Depends(get_device_repository)) -> DeviceUseCases:
    """Get Device use cases instance"""
    return DeviceUseCases(repository)
