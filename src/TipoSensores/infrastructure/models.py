"""
Database models for DeviceType (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, Text
from src.core.db import Base


class DeviceTypeModel(Base):
    __tablename__ = "device_types"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type_name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)  # Permitir NULL en descripción

    def __repr__(self):
        return f"<DeviceTypeModel(id={self.id}, type_name='{self.type_name}')>"
