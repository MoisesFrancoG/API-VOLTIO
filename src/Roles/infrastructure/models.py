"""
Modelos de base de datos para Rol (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.db import Base


class RolModel(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True, index=True)
    descripcion = Column(String(255), nullable=False)

    # Relación con la tabla usuarios
    usuarios = relationship("UsuarioModel", back_populates="rol")

    def __repr__(self):
        return f"<RolModel(id_rol={self.id_rol}, nombre='{self.nombre}')>"
