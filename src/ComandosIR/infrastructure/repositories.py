"""
Implementación del repositorio de ComandosIR usando SQLAlchemy
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from src.ComandosIR.application.interfaces import ComandoIRRepositoryInterface
from src.ComandosIR.domain.schemas import ComandoIRCreate, ComandoIRUpdate, ComandoIRResponse
from src.ComandosIR.infrastructure.models import ComandoIRModel


class SqlAlchemyComandoIRRepository(ComandoIRRepositoryInterface):
    """Implementación del repositorio usando SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ComandoIRResponse]:
        """Obtener todos los comandos IR"""
        comandos_ir = self.db.query(ComandoIRModel).all()
        return [ComandoIRResponse.model_validate(comando) for comando in comandos_ir]

    def get_by_id(self, id_comando: int) -> ComandoIRResponse:
        """Obtener un comando IR por ID"""
        comando_ir = self.db.query(ComandoIRModel).filter(
            ComandoIRModel.id_comando == id_comando
        ).first()
        if not comando_ir:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comando IR con ID {id_comando} no encontrado"
            )
        return ComandoIRResponse.model_validate(comando_ir)

    def get_by_sensor(self, id_sensor: int) -> List[ComandoIRResponse]:
        """Obtener todos los comandos IR de un sensor específico"""
        comandos_ir = self.db.query(ComandoIRModel).filter(
            ComandoIRModel.id_sensor == id_sensor
        ).all()
        return [ComandoIRResponse.model_validate(comando) for comando in comandos_ir]

    def create(self, comando_ir: ComandoIRCreate) -> ComandoIRResponse:
        """Crear un nuevo comando IR"""
        try:
            db_comando_ir = ComandoIRModel(**comando_ir.model_dump())
            self.db.add(db_comando_ir)
            self.db.commit()
            self.db.refresh(db_comando_ir)
            return ComandoIRResponse.model_validate(db_comando_ir)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al crear el comando IR. Verifica que el sensor exista y los datos sean válidos."
            )

    def update(self, id_comando: int, comando_ir: ComandoIRUpdate) -> ComandoIRResponse:
        """Actualizar un comando IR existente"""
        db_comando_ir = self.db.query(ComandoIRModel).filter(
            ComandoIRModel.id_comando == id_comando
        ).first()
        if not db_comando_ir:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comando IR con ID {id_comando} no encontrado"
            )

        # Actualizar solo los campos que no son None
        update_data = comando_ir.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_comando_ir, field, value)

        try:
            self.db.commit()
            self.db.refresh(db_comando_ir)
            return ComandoIRResponse.model_validate(db_comando_ir)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al actualizar el comando IR. Verifica que los datos sean válidos."
            )

    def delete(self, id_comando: int) -> None:
        """Eliminar un comando IR"""
        db_comando_ir = self.db.query(ComandoIRModel).filter(
            ComandoIRModel.id_comando == id_comando
        ).first()
        if not db_comando_ir:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comando IR con ID {id_comando} no encontrado"
            )

        self.db.delete(db_comando_ir)
        self.db.commit()
