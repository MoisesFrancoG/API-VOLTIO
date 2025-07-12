"""
Modelos de base de datos para TipoSensor (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, Text
from src.core.db import Base


class TipoSensorModel(Base):
    __tablename__ = "tipo_sensores"

    id_tipo_sensor = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True, index=True)
    descripcion = Column(Text, nullable=False)

    def __repr__(self):
        return f"<TipoSensorModel(id_tipo_sensor={self.id_tipo_sensor}, nombre='{self.nombre}')>"
