"""
Repositorio SQLAlchemy para el módulo de Lecturas
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc, and_, or_

from ..application.interfaces import LecturaRepository
from ..domain.entities import Lectura
from ..domain.schemas import LecturaCreate, LecturaUpdate
from .models import LecturaModel

class SQLAlchemyLecturaRepository(LecturaRepository):
    """Implementación del repositorio de Lecturas usando SQLAlchemy"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _model_to_entity(self, model: LecturaModel) -> Lectura:
        """Convierte un modelo SQLAlchemy a una entidad de dominio"""
        return Lectura(
            id_lectura=model.id_lectura,
            id_sensor=model.id_sensor,
            valor=model.valor,
            unidad=model.unidad,
            fecha_hora=model.fecha_hora
        )
    
    async def crear_lectura(self, lectura: LecturaCreate) -> Lectura:
        """Crea una nueva lectura"""
        lectura_model = LecturaModel(
            id_sensor=lectura.id_sensor,
            valor=lectura.valor,
            unidad=lectura.unidad,
            fecha_hora=lectura.fecha_hora
        )
        
        self.session.add(lectura_model)
        self.session.commit()
        self.session.refresh(lectura_model)
        
        return self._model_to_entity(lectura_model)
    
    async def obtener_lectura(self, id_lectura: int) -> Optional[Lectura]:
        """Obtiene una lectura por su ID"""
        lectura_model = self.session.query(LecturaModel).filter(LecturaModel.id_lectura == id_lectura).first()
        
        if lectura_model:
            return self._model_to_entity(lectura_model)
        return None
    
    async def obtener_todas_lecturas(self) -> List[Lectura]:
        """Obtiene todas las lecturas"""
        lectura_models = self.session.query(LecturaModel).order_by(desc(LecturaModel.fecha_hora)).all()
        
        return [self._model_to_entity(model) for model in lectura_models]
    
    async def obtener_lecturas_por_sensor(self, id_sensor: int) -> List[Lectura]:
        """Obtiene todas las lecturas de un sensor específico"""
        lectura_models = self.session.query(LecturaModel).filter(
            LecturaModel.id_sensor == id_sensor
        ).order_by(desc(LecturaModel.fecha_hora)).all()
        
        return [self._model_to_entity(model) for model in lectura_models]
    
    async def obtener_lecturas_por_rango_fechas(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Lectura]:
        """Obtiene lecturas dentro de un rango de fechas"""
        lectura_models = self.session.query(LecturaModel).filter(
            and_(
                LecturaModel.fecha_hora >= fecha_inicio,
                LecturaModel.fecha_hora <= fecha_fin
            )
        ).order_by(desc(LecturaModel.fecha_hora)).all()
        
        return [self._model_to_entity(model) for model in lectura_models]
    
    async def obtener_lecturas_por_sensor_y_fechas(self, id_sensor: int, fecha_inicio: datetime, fecha_fin: datetime) -> List[Lectura]:
        """Obtiene lecturas de un sensor específico dentro de un rango de fechas"""
        lectura_models = self.session.query(LecturaModel).filter(
            and_(
                LecturaModel.id_sensor == id_sensor,
                LecturaModel.fecha_hora >= fecha_inicio,
                LecturaModel.fecha_hora <= fecha_fin
            )
        ).order_by(desc(LecturaModel.fecha_hora)).all()
        
        return [self._model_to_entity(model) for model in lectura_models]
    
    async def obtener_lecturas_criticas(self, limite_superior: float = 100.0, limite_inferior: float = 0.0) -> List[Lectura]:
        """Obtiene lecturas que están fuera de los límites normales"""
        lectura_models = self.session.query(LecturaModel).filter(
            or_(LecturaModel.valor > limite_superior, LecturaModel.valor < limite_inferior)
        ).order_by(desc(LecturaModel.fecha_hora)).all()
        
        return [self._model_to_entity(model) for model in lectura_models]
    
    async def obtener_ultimas_lecturas_por_sensor(self, id_sensor: int, limite: int = 10) -> List[Lectura]:
        """Obtiene las últimas N lecturas de un sensor específico"""
        lectura_models = self.session.query(LecturaModel).filter(
            LecturaModel.id_sensor == id_sensor
        ).order_by(desc(LecturaModel.fecha_hora)).limit(limite).all()
        
        return [self._model_to_entity(model) for model in lectura_models]
    
    async def actualizar_lectura(self, id_lectura: int, lectura: LecturaUpdate) -> Optional[Lectura]:
        """Actualiza una lectura existente"""
        lectura_model = self.session.query(LecturaModel).filter(LecturaModel.id_lectura == id_lectura).first()
        
        if not lectura_model:
            return None
        
        # Actualizar solo los campos que no son None
        if lectura.id_sensor is not None:
            lectura_model.id_sensor = lectura.id_sensor
        if lectura.valor is not None:
            lectura_model.valor = lectura.valor
        if lectura.unidad is not None:
            lectura_model.unidad = lectura.unidad
        
        self.session.commit()
        self.session.refresh(lectura_model)
        
        return self._model_to_entity(lectura_model)
    
    async def eliminar_lectura(self, id_lectura: int) -> bool:
        """Elimina una lectura"""
        lectura_model = self.session.query(LecturaModel).filter(LecturaModel.id_lectura == id_lectura).first()
        
        if not lectura_model:
            return False
        
        self.session.delete(lectura_model)
        self.session.commit()
        return True
    
    async def contar_lecturas_por_sensor(self, id_sensor: int) -> int:
        """Cuenta el número de lecturas de un sensor específico"""
        count = self.session.query(func.count(LecturaModel.id_lectura)).filter(LecturaModel.id_sensor == id_sensor).scalar()
        return count or 0
    
    async def obtener_valor_promedio_por_sensor(self, id_sensor: int) -> Optional[float]:
        """Obtiene el valor promedio de las lecturas de un sensor"""
        promedio = self.session.query(func.avg(LecturaModel.valor)).filter(LecturaModel.id_sensor == id_sensor).scalar()
        return float(promedio) if promedio is not None else None
    
    async def obtener_valor_minimo_maximo_por_sensor(self, id_sensor: int) -> Optional[dict]:
        """Obtiene los valores mínimo y máximo de las lecturas de un sensor"""
        result = self.session.query(
            func.min(LecturaModel.valor).label('minimo'),
            func.max(LecturaModel.valor).label('maximo')
        ).filter(LecturaModel.id_sensor == id_sensor).first()
        
        if result and result.minimo is not None and result.maximo is not None:
            return {
                "minimo": float(result.minimo),
                "maximo": float(result.maximo)
            }
        return None
