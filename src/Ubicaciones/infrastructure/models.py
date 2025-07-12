"""
Modelos de base de datos para Ubicacion (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, Text
from src.core.db import Base


class UbicacionModel(Base):
    __tablename__ = "ubicaciones"

    id_ubicacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True, index=True)
    descripcion = Column(Text, nullable=False)

    def __repr__(self):
        return f"<UbicacionModel(id_ubicacion={self.id_ubicacion}, nombre='{self.nombre}')>"
