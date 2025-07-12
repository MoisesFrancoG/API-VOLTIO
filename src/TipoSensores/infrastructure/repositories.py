"""
Implementación del repositorio de TipoSensores usando SQLAlchemy
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from src.TipoSensores.application.interfaces import TipoSensorRepositoryInterface
from src.TipoSensores.domain.schemas import TipoSensorCreate, TipoSensorUpdate, TipoSensorResponse
from src.TipoSensores.infrastructure.models import TipoSensorModel


class SqlAlchemyTipoSensorRepository(TipoSensorRepositoryInterface):
    """Implementación del repositorio usando SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[TipoSensorResponse]:
        """Obtener todos los tipos de sensores"""
        tipos_sensores = self.db.query(TipoSensorModel).all()
        return [TipoSensorResponse.model_validate(tipo_sensor) for tipo_sensor in tipos_sensores]

    def get_by_id(self, id_tipo_sensor: int) -> TipoSensorResponse:
        """Obtener un tipo de sensor por ID"""
        tipo_sensor = self.db.query(TipoSensorModel).filter(
            TipoSensorModel.id_tipo_sensor == id_tipo_sensor
        ).first()
        if not tipo_sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de sensor con ID {id_tipo_sensor} no encontrado"
            )
        return TipoSensorResponse.model_validate(tipo_sensor)

    def create(self, tipo_sensor: TipoSensorCreate) -> TipoSensorResponse:
        """Crear un nuevo tipo de sensor"""
        try:
            db_tipo_sensor = TipoSensorModel(**tipo_sensor.model_dump())
            self.db.add(db_tipo_sensor)
            self.db.commit()
            self.db.refresh(db_tipo_sensor)
            return TipoSensorResponse.model_validate(db_tipo_sensor)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un tipo de sensor con el nombre '{tipo_sensor.nombre}'"
            )

    def update(self, id_tipo_sensor: int, tipo_sensor: TipoSensorUpdate) -> TipoSensorResponse:
        """Actualizar un tipo de sensor existente"""
        db_tipo_sensor = self.db.query(TipoSensorModel).filter(
            TipoSensorModel.id_tipo_sensor == id_tipo_sensor
        ).first()
        if not db_tipo_sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de sensor con ID {id_tipo_sensor} no encontrado"
            )

        # Actualizar solo los campos que no son None
        update_data = tipo_sensor.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_tipo_sensor, field, value)

        try:
            self.db.commit()
            self.db.refresh(db_tipo_sensor)
            return TipoSensorResponse.model_validate(db_tipo_sensor)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un tipo de sensor con el nombre especificado"
            )

    def delete(self, id_tipo_sensor: int) -> None:
        """Eliminar un tipo de sensor"""
        db_tipo_sensor = self.db.query(TipoSensorModel).filter(
            TipoSensorModel.id_tipo_sensor == id_tipo_sensor
        ).first()
        if not db_tipo_sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de sensor con ID {id_tipo_sensor} no encontrado"
            )

        self.db.delete(db_tipo_sensor)
        self.db.commit()
