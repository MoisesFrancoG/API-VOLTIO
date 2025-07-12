"""
Configuración de dependencias específicas para el módulo de TipoSensores
"""

from sqlalchemy.orm import Session
from src.core.db import get_database
from src.TipoSensores.application.use_cases import TipoSensorUseCases
from src.TipoSensores.infrastructure.repositories import SqlAlchemyTipoSensorRepository


def get_tipo_sensor_repository(db: Session) -> SqlAlchemyTipoSensorRepository:
    """Factory para crear instancia del repositorio de TipoSensores"""
    return SqlAlchemyTipoSensorRepository(db)


def get_tipo_sensor_use_cases(db: Session) -> TipoSensorUseCases:
    """Factory para crear instancia de los casos de uso de TipoSensores"""
    repository = get_tipo_sensor_repository(db)
    return TipoSensorUseCases(repository)
