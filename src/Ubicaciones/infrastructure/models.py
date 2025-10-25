"""
Modelos de base de datos para Location (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, Text
from src.core.db import Base


class LocationModel(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f"<LocationModel(id={self.id}, name='{self.name}')>"
