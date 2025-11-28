"""
Database models for DeviceHasCapability (SQLAlchemy)
Pivot table for device-capability many-to-many relationship
"""

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from src.core.db import Base


class DeviceHasCapabilityModel(Base):
    __tablename__ = "device_has_capability"
    __table_args__ = (
        UniqueConstraint('device_id', 'capability_id',
                         name='uq_device_capability'),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey(
        "devices.id", ondelete="CASCADE"), nullable=False, index=True)
    capability_id = Column(Integer, ForeignKey(
        "device_capabilities.id"), nullable=False, index=True)

    # Relationships
    device = relationship("DeviceModel")
    capability = relationship("DeviceCapabilityModel",
                              back_populates="device_capabilities")
    commands = relationship("DeviceCommandModel",
                            back_populates="device_capability_instance")

    def __repr__(self):
        return f"<DeviceHasCapabilityModel(id={self.id}, device_id={self.device_id}, capability_id={self.capability_id})>"
