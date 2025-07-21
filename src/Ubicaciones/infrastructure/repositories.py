"""
Implementación del repositorio de Locations usando SQLAlchemy
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from src.Ubicaciones.application.interfaces import LocationRepositoryInterface
from src.Ubicaciones.domain.schemas import LocationCreate, LocationUpdate, LocationResponse
from src.Ubicaciones.infrastructure.models import LocationModel


class SqlAlchemyLocationRepository(LocationRepositoryInterface):
    """Implementación del repositorio usando SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[LocationResponse]:
        """Obtener todas las ubicaciones"""
        locations = self.db.query(LocationModel).all()
        return [LocationResponse.model_validate(location) for location in locations]

    def get_by_id(self, location_id: int) -> LocationResponse:
        """Obtener una ubicación por ID"""
        location = self.db.query(LocationModel).filter(
            LocationModel.id == location_id
        ).first()
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ubicación con ID {location_id} no encontrada"
            )
        return LocationResponse.model_validate(location)

    def create(self, location: LocationCreate) -> LocationResponse:
        """Crear una nueva ubicación"""
        try:
            db_location = LocationModel(**location.model_dump())
            self.db.add(db_location)
            self.db.commit()
            self.db.refresh(db_location)
            return LocationResponse.model_validate(db_location)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una ubicación con el nombre '{location.name}'"
            )

    def update(self, location_id: int, location: LocationUpdate) -> LocationResponse:
        """Actualizar una ubicación existente"""
        db_location = self.db.query(LocationModel).filter(
            LocationModel.id == location_id
        ).first()
        if not db_location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ubicación con ID {location_id} no encontrada"
            )

        # Actualizar solo los campos que no son None
        update_data = location.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_location, field, value)

        try:
            self.db.commit()
            self.db.refresh(db_location)
            return LocationResponse.model_validate(db_location)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una ubicación con el nombre especificado"
            )

    def delete(self, location_id: int) -> None:
        """Eliminar una ubicación"""
        db_location = self.db.query(LocationModel).filter(
            LocationModel.id == location_id
        ).first()
        if not db_location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ubicación con ID {location_id} no encontrada"
            )

        self.db.delete(db_location)
        self.db.commit()
