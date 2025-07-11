"""
Modelos de base de datos para Usuario (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.core.db import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False, unique=True, index=True)
    contrasena = Column(String(255), nullable=False)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)

    # Relación con la tabla roles
    rol = relationship("RolModel", back_populates="usuarios")

    def __repr__(self):
        return f"<UsuarioModel(id_usuario={self.id_usuario}, nombre_usuario='{self.nombre_usuario}', correo='{self.correo}')>"
