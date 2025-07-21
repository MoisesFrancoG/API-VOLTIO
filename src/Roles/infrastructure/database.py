"""
Configuración de dependencias específicas para el módulo de Roles
"""

from sqlalchemy.orm import Session
from src.core.db import get_database
from src.Roles.application.use_cases import RoleUseCases
from src.Roles.infrastructure.repositories import SqlAlchemyRoleRepository


def get_role_repository(db: Session) -> SqlAlchemyRoleRepository:
    """Factory para crear instancia del repositorio de Roles"""
    return SqlAlchemyRoleRepository(db)


def get_role_use_cases(db: Session) -> RoleUseCases:
    """Factory para crear instancia de los casos de uso de Roles"""
    repository = get_role_repository(db)
    return RoleUseCases(repository)
