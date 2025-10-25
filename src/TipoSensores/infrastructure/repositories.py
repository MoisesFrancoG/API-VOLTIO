"""
DeviceType repository implementation using SQLAlchemy
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from src.TipoSensores.application.interfaces import DeviceTypeRepositoryInterface
from src.TipoSensores.domain.schemas import DeviceTypeCreate, DeviceTypeUpdate, DeviceTypeResponse
from src.TipoSensores.infrastructure.models import DeviceTypeModel


class SqlAlchemyDeviceTypeRepository(DeviceTypeRepositoryInterface):
    """Repository implementation using SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[DeviceTypeResponse]:
        """Get all device types"""
        device_types = self.db.query(DeviceTypeModel).all()
        return [DeviceTypeResponse.model_validate(device_type) for device_type in device_types]

    def get_by_id(self, device_type_id: int) -> DeviceTypeResponse:
        """Get a device type by ID"""
        device_type = self.db.query(DeviceTypeModel).filter(
            DeviceTypeModel.id == device_type_id
        ).first()
        if not device_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Device type with ID {device_type_id} not found"
            )
        return DeviceTypeResponse.model_validate(device_type)

    def create(self, device_type: DeviceTypeCreate) -> DeviceTypeResponse:
        """Create a new device type"""
        try:
            db_device_type = DeviceTypeModel(**device_type.model_dump())
            self.db.add(db_device_type)
            self.db.commit()
            self.db.refresh(db_device_type)
            return DeviceTypeResponse.model_validate(db_device_type)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Device type with name '{device_type.name}' already exists"
            )

    def update(self, device_type_id: int, device_type: DeviceTypeUpdate) -> DeviceTypeResponse:
        """Update an existing device type"""
        db_device_type = self.db.query(DeviceTypeModel).filter(
            DeviceTypeModel.id == device_type_id
        ).first()
        if not db_device_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Device type with ID {device_type_id} not found"
            )

        # Update only non-None fields
        update_data = device_type.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_device_type, field, value)

        try:
            self.db.commit()
            self.db.refresh(db_device_type)
            return DeviceTypeResponse.model_validate(db_device_type)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Device type with the specified name already exists"
            )

    def delete(self, device_type_id: int) -> None:
        """Delete a device type"""
        db_device_type = self.db.query(DeviceTypeModel).filter(
            DeviceTypeModel.id == device_type_id
        ).first()
        if not db_device_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Device type with ID {device_type_id} not found"
            )

        self.db.delete(db_device_type)
        self.db.commit()
