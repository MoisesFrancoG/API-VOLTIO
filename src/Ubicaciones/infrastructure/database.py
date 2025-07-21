"""
Configuración de dependencias específicas para el módulo de Locations
"""

from sqlalchemy.orm import Session
from src.core.db import get_database
from src.Ubicaciones.application.use_cases import LocationUseCases
from src.Ubicaciones.infrastructure.repositories import SqlAlchemyLocationRepository


def get_location_repository(db: Session) -> SqlAlchemyLocationRepository:
    """Factory para crear instancia del repositorio de Locations"""
    return SqlAlchemyLocationRepository(db)


def get_location_use_cases(db: Session) -> LocationUseCases:
    """Factory para crear instancia de los casos de uso de Locations"""
    repository = get_location_repository(db)
    return LocationUseCases(repository)
