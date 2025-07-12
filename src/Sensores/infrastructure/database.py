"""
Configuración de dependencias para el módulo de Sensores
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from ...core.db import get_database
from ..application.use_cases import SensorUseCases
from .repositories import SQLAlchemySensorRepository

def get_sensor_repository(db: Session = Depends(get_database)) -> SQLAlchemySensorRepository:
    """Obtener instancia del repositorio de Sensores"""
    return SQLAlchemySensorRepository(db)

def get_sensor_use_cases(repository: SQLAlchemySensorRepository = Depends(get_sensor_repository)) -> SensorUseCases:
    """Obtener instancia de casos de uso de Sensores"""
    return SensorUseCases(repository)
