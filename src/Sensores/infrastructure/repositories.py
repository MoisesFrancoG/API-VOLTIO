"""
SQLAlchemy repository for the Devices module
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_

from ..application.interfaces import DeviceRepository
from ..domain.entities import Device
from ..domain.schemas import DeviceCreate, DeviceUpdate
from .models import DeviceModel


class SQLAlchemyDeviceRepository(DeviceRepository):
    """Device repository implementation using SQLAlchemy"""

    def __init__(self, session: Session):
        self.session = session

    def _model_to_entity(self, model: DeviceModel) -> Device:
        """Converts a SQLAlchemy model to a domain entity"""
        return Device(
            id=model.id,
            name=model.name,
            device_type_id=model.device_type_id,
            location_id=model.location_id,
            user_id=model.user_id,
            is_active=model.is_active,
            mac_address=getattr(model, 'mac_address', None),
            description=getattr(model, 'description', None),
            created_at=getattr(model, 'created_at', None)
        )

    def create_device(self, device) -> Device:
        """Creates a new device"""
        device_model = DeviceModel(
            name=device.name,
            device_type_id=device.device_type_id,
            location_id=device.location_id,
            user_id=device.user_id,
            is_active=device.is_active,
            mac_address=getattr(device, 'mac_address', None),
            description=getattr(device, 'description', None)
        )

        self.session.add(device_model)
        self.session.commit()
        self.session.refresh(device_model)

        return self._model_to_entity(device_model)

    def get_device(self, device_id: int) -> Optional[Device]:
        """Gets a device by its ID"""
        device_model = self.session.query(DeviceModel).filter(
            DeviceModel.id == device_id).first()

        if device_model:
            return self._model_to_entity(device_model)
        return None

    def get_all_devices(self) -> List[Device]:
        """Gets all devices"""
        device_models = self.session.query(
            DeviceModel).order_by(DeviceModel.name).all()

        return [self._model_to_entity(model) for model in device_models]

    def get_active_devices(self) -> List[Device]:
        """Gets only active devices"""
        device_models = self.session.query(DeviceModel).filter(
            DeviceModel.is_active == True
        ).order_by(DeviceModel.name).all()

        return [self._model_to_entity(model) for model in device_models]

    def get_devices_by_type(self, device_type_id: int) -> List[Device]:
        """Gets devices by type"""
        device_models = self.session.query(DeviceModel).filter(
            DeviceModel.device_type_id == device_type_id
        ).order_by(DeviceModel.name).all()

        return [self._model_to_entity(model) for model in device_models]

    def get_devices_by_location(self, location_id: int) -> List[Device]:
        """Gets devices by location"""
        device_models = self.session.query(DeviceModel).filter(
            DeviceModel.location_id == location_id
        ).order_by(DeviceModel.name).all()

        return [self._model_to_entity(model) for model in device_models]

    def get_devices_by_user(self, user_id: int) -> List[Device]:
        """Gets devices by user"""
        device_models = self.session.query(DeviceModel).filter(
            DeviceModel.user_id == user_id
        ).order_by(DeviceModel.name).all()

        return [self._model_to_entity(model) for model in device_models]

    def search_devices_by_name(self, name: str) -> List[Device]:
        """Searches devices by name (partial search)"""
        device_models = self.session.query(DeviceModel).filter(
            DeviceModel.name.ilike(f"%{name}%")
        ).order_by(DeviceModel.name).all()

        return [self._model_to_entity(model) for model in device_models]

    def update_device(self, device_id: int, device: DeviceUpdate) -> Optional[Device]:
        """Updates an existing device"""
        device_model = self.session.query(DeviceModel).filter(
            DeviceModel.id == device_id).first()

        if not device_model:
            return None

        # Update only non-None fields
        if device.name is not None:
            device_model.name = device.name
        if device.device_type_id is not None:
            device_model.device_type_id = device.device_type_id
        if device.location_id is not None:
            device_model.location_id = device.location_id
        if device.user_id is not None:
            device_model.user_id = device.user_id
        if device.is_active is not None:
            device_model.is_active = device.is_active
        if hasattr(device, 'mac_address') and device.mac_address is not None:
            device_model.mac_address = device.mac_address
        if hasattr(device, 'description') and device.description is not None:
            device_model.description = device.description

        self.session.commit()
        self.session.refresh(device_model)

        return self._model_to_entity(device_model)

    def change_device_status(self, device_id: int, active: bool) -> Optional[Device]:
        """Changes only the active/inactive status of the device"""
        device_model = self.session.query(DeviceModel).filter(
            DeviceModel.id == device_id).first()

        if not device_model:
            return None

        device_model.is_active = active
        self.session.commit()
        self.session.refresh(device_model)

        return self._model_to_entity(device_model)

    def delete_device(self, device_id: int) -> bool:
        """Deletes a device"""
        device_model = self.session.query(DeviceModel).filter(
            DeviceModel.id == device_id).first()

        if not device_model:
            return False

        self.session.delete(device_model)
        self.session.commit()
        return True

    def count_devices_by_type(self, device_type_id: int) -> int:
        """Counts devices by type"""
        count = self.session.query(func.count(DeviceModel.id)).filter(
            DeviceModel.device_type_id == device_type_id
        ).scalar()
        return count or 0

    def count_devices_by_location(self, location_id: int) -> int:
        """Counts devices by location"""
        count = self.session.query(func.count(DeviceModel.id)).filter(
            DeviceModel.location_id == location_id
        ).scalar()
        return count or 0

    def count_devices_by_user(self, user_id: int) -> int:
        """Counts devices by user"""
        count = self.session.query(func.count(DeviceModel.id)).filter(
            DeviceModel.user_id == user_id
        ).scalar()
        return count or 0

    def exists_device_with_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Checks if a device with the given name exists"""
        query = self.session.query(DeviceModel).filter(
            DeviceModel.name == name)

        if exclude_id:
            query = query.filter(DeviceModel.id != exclude_id)

        return query.first() is not None

    def exists_device_with_mac(self, mac_address: str, exclude_id: Optional[int] = None) -> bool:
        """Checks if a device with the given MAC address exists"""
        query = self.session.query(DeviceModel).filter(
            DeviceModel.mac_address == mac_address)

        if exclude_id:
            query = query.filter(DeviceModel.id != exclude_id)

        return query.first() is not None

    def get_by_mac_address(self, mac_address: str) -> Optional[Device]:
        """Gets a device by its MAC address"""
        device_model = self.session.query(DeviceModel).filter(
            DeviceModel.mac_address == mac_address).first()

        if device_model:
            return self._model_to_entity(device_model)
        return None

    def get_device_with_type_by_mac(self, mac_address: str) -> Optional[dict]:
        """Gets a device with type information by MAC address"""
        from src.TipoSensores.infrastructure.models import DeviceTypeModel

        result = self.session.query(
            DeviceModel,
            DeviceTypeModel.type_name
        ).join(
            DeviceTypeModel, DeviceModel.device_type_id == DeviceTypeModel.id
        ).filter(
            DeviceModel.mac_address == mac_address
        ).first()

        if result:
            device_model, type_name = result
            return {
                'device': self._model_to_entity(device_model),
                'type_name': type_name
            }
        return None
