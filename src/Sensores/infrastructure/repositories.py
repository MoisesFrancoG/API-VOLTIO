"""
Repositorio SQLAlchemy para el módulo de Sensores
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_

from ..application.interfaces import SensorRepository
from ..domain.entities import Sensor
from ..domain.schemas import SensorCreate, SensorUpdate
from .models import SensorModel

class SQLAlchemySensorRepository(SensorRepository):
    """Implementación del repositorio de Sensores usando SQLAlchemy"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _model_to_entity(self, model: SensorModel) -> Sensor:
        """Convierte un modelo SQLAlchemy a una entidad de dominio"""
        return Sensor(
            id_sensor=model.id_sensor,
            nombre=model.nombre,
            id_tipo_sensor=model.id_tipo_sensor,
            id_ubicacion=model.id_ubicacion,
            id_usuario=model.id_usuario,
            activo=model.activo
        )
    
    def crear_sensor(self, sensor: SensorCreate) -> Sensor:
        """Crea un nuevo sensor"""
        sensor_model = SensorModel(
            nombre=sensor.nombre,
            id_tipo_sensor=sensor.id_tipo_sensor,
            id_ubicacion=sensor.id_ubicacion,
            id_usuario=sensor.id_usuario,
            activo=sensor.activo
        )
        
        self.session.add(sensor_model)
        self.session.commit()
        self.session.refresh(sensor_model)
        
        return self._model_to_entity(sensor_model)
    
    def obtener_sensor(self, id_sensor: int) -> Optional[Sensor]:
        """Obtiene un sensor por su ID"""
        sensor_model = self.session.query(SensorModel).filter(SensorModel.id_sensor == id_sensor).first()
        
        if sensor_model:
            return self._model_to_entity(sensor_model)
        return None
    
    def obtener_todos_sensores(self) -> List[Sensor]:
        """Obtiene todos los sensores"""
        sensor_models = self.session.query(SensorModel).order_by(SensorModel.nombre).all()
        
        return [self._model_to_entity(model) for model in sensor_models]
    
    def obtener_sensores_activos(self) -> List[Sensor]:
        """Obtiene solo los sensores activos"""
        sensor_models = self.session.query(SensorModel).filter(
            SensorModel.activo == True
        ).order_by(SensorModel.nombre).all()
        
        return [self._model_to_entity(model) for model in sensor_models]
    
    def obtener_sensores_por_tipo(self, id_tipo_sensor: int) -> List[Sensor]:
        """Obtiene sensores por tipo"""
        sensor_models = self.session.query(SensorModel).filter(
            SensorModel.id_tipo_sensor == id_tipo_sensor
        ).order_by(SensorModel.nombre).all()
        
        return [self._model_to_entity(model) for model in sensor_models]
    
    def obtener_sensores_por_ubicacion(self, id_ubicacion: int) -> List[Sensor]:
        """Obtiene sensores por ubicación"""
        sensor_models = self.session.query(SensorModel).filter(
            SensorModel.id_ubicacion == id_ubicacion
        ).order_by(SensorModel.nombre).all()
        
        return [self._model_to_entity(model) for model in sensor_models]
    
    def obtener_sensores_por_usuario(self, id_usuario: int) -> List[Sensor]:
        """Obtiene sensores por usuario"""
        sensor_models = self.session.query(SensorModel).filter(
            SensorModel.id_usuario == id_usuario
        ).order_by(SensorModel.nombre).all()
        
        return [self._model_to_entity(model) for model in sensor_models]
    
    def buscar_sensores_por_nombre(self, nombre: str) -> List[Sensor]:
        """Busca sensores por nombre (búsqueda parcial)"""
        sensor_models = self.session.query(SensorModel).filter(
            SensorModel.nombre.ilike(f"%{nombre}%")
        ).order_by(SensorModel.nombre).all()
        
        return [self._model_to_entity(model) for model in sensor_models]
    
    def actualizar_sensor(self, id_sensor: int, sensor: SensorUpdate) -> Optional[Sensor]:
        """Actualiza un sensor existente"""
        sensor_model = self.session.query(SensorModel).filter(SensorModel.id_sensor == id_sensor).first()
        
        if not sensor_model:
            return None
        
        # Actualizar solo los campos que no son None
        if sensor.nombre is not None:
            sensor_model.nombre = sensor.nombre
        if sensor.id_tipo_sensor is not None:
            sensor_model.id_tipo_sensor = sensor.id_tipo_sensor
        if sensor.id_ubicacion is not None:
            sensor_model.id_ubicacion = sensor.id_ubicacion
        if sensor.id_usuario is not None:
            sensor_model.id_usuario = sensor.id_usuario
        if sensor.activo is not None:
            sensor_model.activo = sensor.activo
        
        self.session.commit()
        self.session.refresh(sensor_model)
        
        return self._model_to_entity(sensor_model)
    
    def cambiar_estado_sensor(self, id_sensor: int, activo: bool) -> Optional[Sensor]:
        """Cambia solo el estado activo/inactivo del sensor"""
        sensor_model = self.session.query(SensorModel).filter(SensorModel.id_sensor == id_sensor).first()
        
        if not sensor_model:
            return None
        
        sensor_model.activo = activo
        self.session.commit()
        self.session.refresh(sensor_model)
        
        return self._model_to_entity(sensor_model)
    
    def eliminar_sensor(self, id_sensor: int) -> bool:
        """Elimina un sensor"""
        sensor_model = self.session.query(SensorModel).filter(SensorModel.id_sensor == id_sensor).first()
        
        if not sensor_model:
            return False
        
        self.session.delete(sensor_model)
        self.session.commit()
        return True
    
    def contar_sensores_por_tipo(self, id_tipo_sensor: int) -> int:
        """Cuenta sensores por tipo"""
        count = self.session.query(func.count(SensorModel.id_sensor)).filter(
            SensorModel.id_tipo_sensor == id_tipo_sensor
        ).scalar()
        return count or 0
    
    def contar_sensores_por_ubicacion(self, id_ubicacion: int) -> int:
        """Cuenta sensores por ubicación"""
        count = self.session.query(func.count(SensorModel.id_sensor)).filter(
            SensorModel.id_ubicacion == id_ubicacion
        ).scalar()
        return count or 0
    
    def contar_sensores_por_usuario(self, id_usuario: int) -> int:
        """Cuenta sensores por usuario"""
        count = self.session.query(func.count(SensorModel.id_sensor)).filter(
            SensorModel.id_usuario == id_usuario
        ).scalar()
        return count or 0
    
    def existe_sensor_con_nombre(self, nombre: str, excluir_id: Optional[int] = None) -> bool:
        """Verifica si existe un sensor con el nombre dado"""
        query = self.session.query(SensorModel).filter(SensorModel.nombre == nombre)
        
        if excluir_id:
            query = query.filter(SensorModel.id_sensor != excluir_id)
        
        return query.first() is not None
