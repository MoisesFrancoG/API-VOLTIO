"""
Configuración de dependencias específicas para el módulo de ComandosIR
"""

from sqlalchemy.orm import Session
from src.core.db import get_database
from src.ComandosIR.application.use_cases import ComandoIRUseCases
from src.ComandosIR.infrastructure.repositories import SqlAlchemyComandoIRRepository


def get_comando_ir_repository(db: Session) -> SqlAlchemyComandoIRRepository:
    """Factory para crear instancia del repositorio de ComandosIR"""
    return SqlAlchemyComandoIRRepository(db)


def get_comando_ir_use_cases(db: Session) -> ComandoIRUseCases:
    """Factory para crear instancia de los casos de uso de ComandosIR"""
    repository = get_comando_ir_repository(db)
    return ComandoIRUseCases(repository)
