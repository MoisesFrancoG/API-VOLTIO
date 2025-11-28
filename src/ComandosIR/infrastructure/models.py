"""
Database models for DeviceCommand (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.core.db import Base


class DeviceCommandModel(Base):
    __tablename__ = "device_commands"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_capability_instance_id = Column(
        Integer, ForeignKey("device_has_capability.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    command_payload = Column(Text, nullable=False)

    # Relationship
    device_capability_instance = relationship(
        "DeviceHasCapabilityModel", back_populates="commands")

    def __repr__(self):
        return f"<DeviceCommandModel(id={self.id}, name='{self.name}', device={self.device_id})>"
