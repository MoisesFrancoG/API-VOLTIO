"""
Implementation of DeviceCommand repository using SQLAlchemy
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from src.ComandosIR.application.interfaces import DeviceCommandRepositoryInterface
from src.ComandosIR.domain.schemas import DeviceCommandCreate, DeviceCommandUpdate, DeviceCommandResponse
from src.ComandosIR.infrastructure.models import DeviceCommandModel


class SqlAlchemyDeviceCommandRepository(DeviceCommandRepositoryInterface):
    """Implementation of the repository using SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[DeviceCommandResponse]:
        """Get all device commands"""
        device_commands = self.db.query(DeviceCommandModel).all()
        return [DeviceCommandResponse.model_validate(command) for command in device_commands]

    def get_by_id(self, id: int) -> DeviceCommandResponse:
        """Get a device command by ID"""
        device_command = self.db.query(DeviceCommandModel).filter(
            DeviceCommandModel.id == id
        ).first()
        if not device_command:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Device command with ID {id} not found"
            )
        return DeviceCommandResponse.model_validate(device_command)

    def get_by_device(self, device_id: int) -> List[DeviceCommandResponse]:
        """Get all device commands for a specific device"""
        device_commands = self.db.query(DeviceCommandModel).filter(
            DeviceCommandModel.device_id == device_id
        ).all()
        return [DeviceCommandResponse.model_validate(command) for command in device_commands]

    def create(self, device_command: DeviceCommandCreate) -> DeviceCommandResponse:
        """Create a new device command"""
        try:
            db_device_command = DeviceCommandModel(
                **device_command.model_dump())
            self.db.add(db_device_command)
            self.db.commit()
            self.db.refresh(db_device_command)
            return DeviceCommandResponse.model_validate(db_device_command)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating device command. Verify that the device exists and the data is valid."
            )

    def update(self, id: int, device_command: DeviceCommandUpdate) -> DeviceCommandResponse:
        """Update an existing device command"""
        db_device_command = self.db.query(DeviceCommandModel).filter(
            DeviceCommandModel.id == id
        ).first()
        if not db_device_command:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Device command with ID {id} not found"
            )

        # Update only fields that are not None
        update_data = device_command.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_device_command, field, value)

        try:
            self.db.commit()
            self.db.refresh(db_device_command)
            return DeviceCommandResponse.model_validate(db_device_command)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error updating device command. Verify that the data is valid."
            )

    def delete(self, id: int) -> None:
        """Delete a device command"""
        db_device_command = self.db.query(DeviceCommandModel).filter(
            DeviceCommandModel.id == id
        ).first()
        if not db_device_command:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Device command with ID {id} not found"
            )

        self.db.delete(db_device_command)
        self.db.commit()
