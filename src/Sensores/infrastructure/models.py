"""
Modelos SQLAlchemy para el módulo de Sensores
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ...core.db import Base

class SensorModel(Base):
    """Modelo SQLAlchemy para Sensor"""
    
    __tablename__ = "sensores"
    
    id_sensor = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True, index=True)
    id_tipo_sensor = Column(Integer, nullable=False, index=True)  # FK a tipo_sensores
    id_ubicacion = Column(Integer, nullable=False, index=True)    # FK a ubicaciones
    id_usuario = Column(Integer, nullable=False, index=True)      # FK a usuarios
    activo = Column(Boolean, default=True, nullable=False, index=True)
    
    # Relaciones con otros modelos (cuando estén disponibles)
    # tipo_sensor = relationship("TipoSensorModel", back_populates="sensores")
    # ubicacion = relationship("UbicacionModel", back_populates="sensores")
    # usuario = relationship("UsuarioModel", back_populates="sensores")
    # lecturas = relationship("LecturaModel", back_populates="sensor")
    # comandos_ir = relationship("ComandoIRModel", back_populates="sensor")
    
    def __repr__(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"<SensorModel(id_sensor={self.id_sensor}, nombre='{self.nombre}', tipo={self.id_tipo_sensor}, ubicacion={self.id_ubicacion}, usuario={self.id_usuario}, estado={estado})>"
