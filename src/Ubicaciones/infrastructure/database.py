"""
Configuración de dependencias específicas para el módulo de Ubicaciones
"""

from sqlalchemy.orm import Session
from src.core.db import get_database
from src.Ubicaciones.application.use_cases import UbicacionUseCases
from src.Ubicaciones.infrastructure.repositories import SqlAlchemyUbicacionRepository


def get_ubicacion_repository(db: Session) -> SqlAlchemyUbicacionRepository:
    """Factory para crear instancia del repositorio de Ubicaciones"""
    return SqlAlchemyUbicacionRepository(db)


def get_ubicacion_use_cases(db: Session) -> UbicacionUseCases:
    """Factory para crear instancia de los casos de uso de Ubicaciones"""
    repository = get_ubicacion_repository(db)
    return UbicacionUseCases(repository)
