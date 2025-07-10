"""
Configuración de dependencias específicas para el módulo de Roles
"""

from sqlalchemy.orm import Session
from src.core.db import get_database
from src.Roles.application.use_cases import RolUseCases
from src.Roles.infrastructure.repositories import SqlAlchemyRolRepository


def get_rol_repository(db: Session) -> SqlAlchemyRolRepository:
    """Factory para crear instancia del repositorio de Roles"""
    return SqlAlchemyRolRepository(db)


def get_rol_use_cases(db: Session) -> RolUseCases:
    """Factory para crear instancia de los casos de uso de Roles"""
    repository = get_rol_repository(db)
    return RolUseCases(repository)
