"""
Database models for DeviceCapability (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from src.core.db import Base


class DeviceCapabilityModel(Base):
    __tablename__ = "device_capabilities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    capability_name = Column(
        String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    is_actionable = Column(Boolean, default=False, nullable=False)

    # Relationships
    device_capabilities = relationship(
        "DeviceHasCapabilityModel", back_populates="capability")

    def __repr__(self):
        return f"<DeviceCapabilityModel(id={self.id}, name='{self.capability_name}', actionable={self.is_actionable})>"
