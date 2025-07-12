"""
Modelos de base de datos para Alerta (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from sqlalchemy.sql import func
from src.core.db import Base


class AlertaModel(Base):
    __tablename__ = "alertas"

    id_alerta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_lectura = Column(Integer, nullable=False, index=True)  # ForeignKey se agregará cuando exista la tabla lecturas
    tipo_alerta = Column(String(100), nullable=False, index=True)
    descripcion = Column(Text, nullable=False)
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # Índices compuestos para optimizar consultas comunes
    __table_args__ = (
        Index('idx_alertas_tipo_fecha', 'tipo_alerta', 'fecha_hora'),
        Index('idx_alertas_lectura_fecha', 'id_lectura', 'fecha_hora'),
    )

    # Nota: La relación con lecturas se agregará cuando se implemente el módulo correspondiente
    # lectura = relationship("LecturaModel", back_populates="alertas")

    def __repr__(self):
        return f"<AlertaModel(id_alerta={self.id_alerta}, tipo='{self.tipo_alerta}', lectura={self.id_lectura}, fecha={self.fecha_hora})>"
