"""
Modelos de base de datos para ComandoIR (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.core.db import Base


class ComandoIRModel(Base):
    __tablename__ = "comandos_ir"

    id_comando = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_sensor = Column(Integer, nullable=False, index=True)  # ForeignKey se agregará cuando exista la tabla sensores
    nombre = Column(String(100), nullable=False, index=True)
    descripcion = Column(Text, nullable=False)
    comando = Column(String(255), nullable=False)

    # Nota: La relación con sensores se agregará cuando se implemente el módulo Sensores
    # sensor = relationship("SensorModel", back_populates="comandos_ir")

    def __repr__(self):
        return f"<ComandoIRModel(id_comando={self.id_comando}, nombre='{self.nombre}', sensor={self.id_sensor})>"
