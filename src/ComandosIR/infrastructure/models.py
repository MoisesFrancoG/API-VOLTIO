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
        Integer, nullable=False, index=True)  # ForeignKey to devices table
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    command_payload = Column(String(255), nullable=False)

    # Note: Relationship with devices will be added when both modules are fully integrated
    # device = relationship("DeviceModel", back_populates="device_commands")

    def __repr__(self):
        return f"<DeviceCommandModel(id={self.id}, name='{self.name}', device={self.device_id})>"
