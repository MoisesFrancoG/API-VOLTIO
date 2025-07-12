"""
Interfaces (puertos) para el módulo de Lecturas
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from ..domain.entities import Lectura
from ..domain.schemas import LecturaCreate, LecturaUpdate

class LecturaRepository(ABC):
    """Interfaz abstracta para el repositorio de Lecturas"""
    
    @abstractmethod
    async def crear_lectura(self, lectura: LecturaCreate) -> Lectura:
        """Crea una nueva lectura"""
        pass
    
    @abstractmethod
    async def obtener_lectura(self, id_lectura: int) -> Optional[Lectura]:
        """Obtiene una lectura por su ID"""
        pass
    
    @abstractmethod
    async def obtener_todas_lecturas(self) -> List[Lectura]:
        """Obtiene todas las lecturas"""
        pass
    
    @abstractmethod
    async def obtener_lecturas_por_sensor(self, id_sensor: int) -> List[Lectura]:
        """Obtiene todas las lecturas de un sensor específico"""
        pass
    
    @abstractmethod
    async def obtener_lecturas_por_rango_fechas(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Lectura]:
        """Obtiene lecturas dentro de un rango de fechas"""
        pass
    
    @abstractmethod
    async def obtener_lecturas_por_sensor_y_fechas(self, id_sensor: int, fecha_inicio: datetime, fecha_fin: datetime) -> List[Lectura]:
        """Obtiene lecturas de un sensor específico dentro de un rango de fechas"""
        pass
    
    @abstractmethod
    async def obtener_lecturas_criticas(self, limite_superior: float = 100.0, limite_inferior: float = 0.0) -> List[Lectura]:
        """Obtiene lecturas que están fuera de los límites normales"""
        pass
    
    @abstractmethod
    async def obtener_ultimas_lecturas_por_sensor(self, id_sensor: int, limite: int = 10) -> List[Lectura]:
        """Obtiene las últimas N lecturas de un sensor específico"""
        pass
    
    @abstractmethod
    async def actualizar_lectura(self, id_lectura: int, lectura: LecturaUpdate) -> Optional[Lectura]:
        """Actualiza una lectura existente"""
        pass
    
    @abstractmethod
    async def eliminar_lectura(self, id_lectura: int) -> bool:
        """Elimina una lectura"""
        pass
    
    @abstractmethod
    async def contar_lecturas_por_sensor(self, id_sensor: int) -> int:
        """Cuenta el número de lecturas de un sensor específico"""
        pass
    
    @abstractmethod
    async def obtener_valor_promedio_por_sensor(self, id_sensor: int) -> Optional[float]:
        """Obtiene el valor promedio de las lecturas de un sensor"""
        pass
    
    @abstractmethod
    async def obtener_valor_minimo_maximo_por_sensor(self, id_sensor: int) -> Optional[dict]:
        """Obtiene los valores mínimo y máximo de las lecturas de un sensor"""
        pass
