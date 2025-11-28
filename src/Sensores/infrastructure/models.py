"""
SQLAlchemy models for the Devices module
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ...core.db import Base


class DeviceModel(Base):
    """SQLAlchemy model for Device"""

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=True, index=True)
    device_type_id = Column(Integer, ForeignKey(
        "device_types.id"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=True, index=True)
    mac_address = Column(String(17), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    location_id = Column(Integer, ForeignKey(
        "locations.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)

    # Relationships with other models (when available)
    # device_type = relationship("DeviceTypeModel", back_populates="devices")
    # location = relationship("LocationModel", back_populates="devices")
    # user = relationship("UserModel", back_populates="devices")
    # readings = relationship("ReadingModel", back_populates="device")
    # ir_commands = relationship("IRCommandModel", back_populates="device")

    # Relación con notificaciones
    notifications = relationship("NotificationModel", back_populates="device")

    def __repr__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"<DeviceModel(id={self.id}, name='{self.name}', type={self.device_type_id}, user={self.user_id}, status={status})>"
