"""
Configuración de dependencias específicas para el módulo de Usuarios
"""

from sqlalchemy.orm import Session
from src.core.db import get_database
from src.Usuarios.application.use_cases import UsuarioUseCases
from src.Usuarios.infrastructure.repositories import SqlAlchemyUsuarioRepository


def get_usuario_repository(db: Session) -> SqlAlchemyUsuarioRepository:
    """Obtener instancia del repositorio de usuarios"""
    return SqlAlchemyUsuarioRepository(db)


def get_usuario_use_cases(db: Session) -> UsuarioUseCases:
    """Obtener instancia de los casos de uso de usuarios"""
    repository = get_usuario_repository(db)
    return UsuarioUseCases(repository)
