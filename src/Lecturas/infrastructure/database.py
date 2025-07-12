"""
Configuración de dependencias para el módulo de Lecturas
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from ...core.db import get_database
from ..application.use_cases import LecturaUseCases
from .repositories import SQLAlchemyLecturaRepository

def get_lectura_repository(db: Session = Depends(get_database)) -> SQLAlchemyLecturaRepository:
    """Obtener instancia del repositorio de Lecturas"""
    return SQLAlchemyLecturaRepository(db)

def get_lectura_use_cases(repository: SQLAlchemyLecturaRepository = Depends(get_lectura_repository)) -> LecturaUseCases:
    """Obtener instancia de casos de uso de Lecturas"""
    return LecturaUseCases(repository)
