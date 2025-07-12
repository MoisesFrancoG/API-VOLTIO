"""
Modelos SQLAlchemy para el módulo de Lecturas
"""

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime

from ...core.db import Base

class LecturaModel(Base):
    """Modelo SQLAlchemy para Lectura"""
    
    __tablename__ = "lecturas"
    
    id_lectura = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_sensor = Column(Integer, nullable=False, index=True)  # Removemos ForeignKey temporalmente
    valor = Column(Float, nullable=False)
    unidad = Column(String(10), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.now, nullable=False, index=True)
    
    # Relación con el modelo de Sensor (cuando esté disponible)
    # sensor = relationship("SensorModel", back_populates="lecturas")
    
    def __repr__(self):
        return f"<LecturaModel(id_lectura={self.id_lectura}, id_sensor={self.id_sensor}, valor={self.valor}, unidad='{self.unidad}', fecha_hora={self.fecha_hora})>"
