"""
Implementación del repositorio de Ubicaciones usando SQLAlchemy
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from src.Ubicaciones.application.interfaces import UbicacionRepositoryInterface
from src.Ubicaciones.domain.schemas import UbicacionCreate, UbicacionUpdate, UbicacionResponse
from src.Ubicaciones.infrastructure.models import UbicacionModel


class SqlAlchemyUbicacionRepository(UbicacionRepositoryInterface):
    """Implementación del repositorio usando SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[UbicacionResponse]:
        """Obtener todas las ubicaciones"""
        ubicaciones = self.db.query(UbicacionModel).all()
        return [UbicacionResponse.model_validate(ubicacion) for ubicacion in ubicaciones]

    def get_by_id(self, id_ubicacion: int) -> UbicacionResponse:
        """Obtener una ubicación por ID"""
        ubicacion = self.db.query(UbicacionModel).filter(
            UbicacionModel.id_ubicacion == id_ubicacion
        ).first()
        if not ubicacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ubicación con ID {id_ubicacion} no encontrada"
            )
        return UbicacionResponse.model_validate(ubicacion)

    def create(self, ubicacion: UbicacionCreate) -> UbicacionResponse:
        """Crear una nueva ubicación"""
        try:
            db_ubicacion = UbicacionModel(**ubicacion.model_dump())
            self.db.add(db_ubicacion)
            self.db.commit()
            self.db.refresh(db_ubicacion)
            return UbicacionResponse.model_validate(db_ubicacion)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una ubicación con el nombre '{ubicacion.nombre}'"
            )

    def update(self, id_ubicacion: int, ubicacion: UbicacionUpdate) -> UbicacionResponse:
        """Actualizar una ubicación existente"""
        db_ubicacion = self.db.query(UbicacionModel).filter(
            UbicacionModel.id_ubicacion == id_ubicacion
        ).first()
        if not db_ubicacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ubicación con ID {id_ubicacion} no encontrada"
            )

        # Actualizar solo los campos que no son None
        update_data = ubicacion.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_ubicacion, field, value)

        try:
            self.db.commit()
            self.db.refresh(db_ubicacion)
            return UbicacionResponse.model_validate(db_ubicacion)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una ubicación con el nombre especificado"
            )

    def delete(self, id_ubicacion: int) -> None:
        """Eliminar una ubicación"""
        db_ubicacion = self.db.query(UbicacionModel).filter(
            UbicacionModel.id_ubicacion == id_ubicacion
        ).first()
        if not db_ubicacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ubicación con ID {id_ubicacion} no encontrada"
            )

        self.db.delete(db_ubicacion)
        self.db.commit()
