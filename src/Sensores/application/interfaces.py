"""
Interfaces (puertos) para el módulo de Sensores
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..domain.entities import Sensor
from ..domain.schemas import SensorCreate, SensorUpdate

class SensorRepository(ABC):
    """Interfaz abstracta para el repositorio de Sensores"""
    
    @abstractmethod
    def crear_sensor(self, sensor: SensorCreate) -> Sensor:
        """Crea un nuevo sensor"""
        pass
    
    @abstractmethod
    def obtener_sensor(self, id_sensor: int) -> Optional[Sensor]:
        """Obtiene un sensor por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos_sensores(self) -> List[Sensor]:
        """Obtiene todos los sensores"""
        pass
    
    @abstractmethod
    def obtener_sensores_activos(self) -> List[Sensor]:
        """Obtiene solo los sensores activos"""
        pass
    
    @abstractmethod
    def obtener_sensores_por_tipo(self, id_tipo_sensor: int) -> List[Sensor]:
        """Obtiene sensores por tipo"""
        pass
    
    @abstractmethod
    def obtener_sensores_por_ubicacion(self, id_ubicacion: int) -> List[Sensor]:
        """Obtiene sensores por ubicación"""
        pass
    
    @abstractmethod
    def obtener_sensores_por_usuario(self, id_usuario: int) -> List[Sensor]:
        """Obtiene sensores por usuario"""
        pass
    
    @abstractmethod
    def buscar_sensores_por_nombre(self, nombre: str) -> List[Sensor]:
        """Busca sensores por nombre (búsqueda parcial)"""
        pass
    
    @abstractmethod
    def actualizar_sensor(self, id_sensor: int, sensor: SensorUpdate) -> Optional[Sensor]:
        """Actualiza un sensor existente"""
        pass
    
    @abstractmethod
    def cambiar_estado_sensor(self, id_sensor: int, activo: bool) -> Optional[Sensor]:
        """Cambia solo el estado activo/inactivo del sensor"""
        pass
    
    @abstractmethod
    def eliminar_sensor(self, id_sensor: int) -> bool:
        """Elimina un sensor"""
        pass
    
    @abstractmethod
    def contar_sensores_por_tipo(self, id_tipo_sensor: int) -> int:
        """Cuenta sensores por tipo"""
        pass
    
    @abstractmethod
    def contar_sensores_por_ubicacion(self, id_ubicacion: int) -> int:
        """Cuenta sensores por ubicación"""
        pass
    
    @abstractmethod
    def contar_sensores_por_usuario(self, id_usuario: int) -> int:
        """Cuenta sensores por usuario"""
        pass
    
    @abstractmethod
    def existe_sensor_con_nombre(self, nombre: str, excluir_id: Optional[int] = None) -> bool:
        """Verifica si existe un sensor con el nombre dado"""
        pass
