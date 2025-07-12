"""
Implementación del repositorio de Alertas usando SQLAlchemy
"""

from typing import List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, and_
from fastapi import HTTPException, status

from src.Alertas.application.interfaces import AlertaRepositoryInterface
from src.Alertas.domain.schemas import AlertaCreate, AlertaUpdate, AlertaResponse
from src.Alertas.infrastructure.models import AlertaModel


class SqlAlchemyAlertaRepository(AlertaRepositoryInterface):
    """Implementación del repositorio usando SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[AlertaResponse]:
        """Obtener todas las alertas ordenadas por fecha descendente"""
        alertas = self.db.query(AlertaModel).order_by(desc(AlertaModel.fecha_hora)).all()
        return [AlertaResponse.model_validate(alerta) for alerta in alertas]

    def get_by_id(self, id_alerta: int) -> AlertaResponse:
        """Obtener una alerta por ID"""
        alerta = self.db.query(AlertaModel).filter(
            AlertaModel.id_alerta == id_alerta
        ).first()
        if not alerta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alerta con ID {id_alerta} no encontrada"
            )
        return AlertaResponse.model_validate(alerta)

    def get_by_lectura(self, id_lectura: int) -> List[AlertaResponse]:
        """Obtener todas las alertas de una lectura específica"""
        alertas = self.db.query(AlertaModel).filter(
            AlertaModel.id_lectura == id_lectura
        ).order_by(desc(AlertaModel.fecha_hora)).all()
        return [AlertaResponse.model_validate(alerta) for alerta in alertas]

    def get_by_tipo(self, tipo_alerta: str) -> List[AlertaResponse]:
        """Obtener todas las alertas de un tipo específico"""
        alertas = self.db.query(AlertaModel).filter(
            AlertaModel.tipo_alerta == tipo_alerta.upper()
        ).order_by(desc(AlertaModel.fecha_hora)).all()
        return [AlertaResponse.model_validate(alerta) for alerta in alertas]

    def get_criticas(self) -> List[AlertaResponse]:
        """Obtener todas las alertas críticas"""
        alertas = self.db.query(AlertaModel).filter(
            AlertaModel.tipo_alerta == "CRITICA"
        ).order_by(desc(AlertaModel.fecha_hora)).all()
        return [AlertaResponse.model_validate(alerta) for alerta in alertas]

    def get_recientes(self, horas: int = 24) -> List[AlertaResponse]:
        """Obtener alertas recientes (últimas X horas)"""
        fecha_limite = datetime.now() - timedelta(hours=horas)
        alertas = self.db.query(AlertaModel).filter(
            AlertaModel.fecha_hora >= fecha_limite
        ).order_by(desc(AlertaModel.fecha_hora)).all()
        return [AlertaResponse.model_validate(alerta) for alerta in alertas]

    def create(self, alerta: AlertaCreate) -> AlertaResponse:
        """Crear una nueva alerta"""
        try:
            # Crear el modelo con los datos del esquema
            alerta_data = alerta.model_dump()
            db_alerta = AlertaModel(**alerta_data)
            
            self.db.add(db_alerta)
            self.db.commit()
            self.db.refresh(db_alerta)
            return AlertaResponse.model_validate(db_alerta)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al crear la alerta. Verifica que la lectura exista y los datos sean válidos."
            )

    def update(self, id_alerta: int, alerta: AlertaUpdate) -> AlertaResponse:
        """Actualizar una alerta existente"""
        db_alerta = self.db.query(AlertaModel).filter(
            AlertaModel.id_alerta == id_alerta
        ).first()
        if not db_alerta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alerta con ID {id_alerta} no encontrada"
            )

        # Actualizar solo los campos que no son None
        update_data = alerta.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_alerta, field, value)

        try:
            self.db.commit()
            self.db.refresh(db_alerta)
            return AlertaResponse.model_validate(db_alerta)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al actualizar la alerta. Verifica que los datos sean válidos."
            )

    def delete(self, id_alerta: int) -> None:
        """Eliminar una alerta"""
        db_alerta = self.db.query(AlertaModel).filter(
            AlertaModel.id_alerta == id_alerta
        ).first()
        if not db_alerta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alerta con ID {id_alerta} no encontrada"
            )

        self.db.delete(db_alerta)
        self.db.commit()
