"""
Configuración de dependencias específicas para el módulo de Usuarios
"""

from sqlalchemy.orm import Session
from src.core.db import get_database
from src.Usuarios.application.use_cases import UserUseCases
from src.Usuarios.infrastructure.repositories import SqlAlchemyUserRepository


def get_user_repository(db: Session) -> SqlAlchemyUserRepository:
    """Obtener instancia del repositorio de usuarios"""
    return SqlAlchemyUserRepository(db)


def get_user_use_cases(db: Session) -> UserUseCases:
    """Obtener instancia de los casos de uso de usuarios"""
    repository = get_user_repository(db)
    return UserUseCases(repository)
