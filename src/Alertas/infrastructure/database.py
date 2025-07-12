"""
Configuración de dependencias específicas para el módulo de Alertas
"""

from sqlalchemy.orm import Session
from src.core.db import get_database
from src.Alertas.application.use_cases import AlertaUseCases
from src.Alertas.infrastructure.repositories import SqlAlchemyAlertaRepository


def get_alerta_repository(db: Session) -> SqlAlchemyAlertaRepository:
    """Factory para crear instancia del repositorio de Alertas"""
    return SqlAlchemyAlertaRepository(db)


def get_alerta_use_cases(db: Session) -> AlertaUseCases:
    """Factory para crear instancia de los casos de uso de Alertas"""
    repository = get_alerta_repository(db)
    return AlertaUseCases(repository)
