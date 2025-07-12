"""
Casos de uso para el módulo de Lecturas
"""

from typing import List, Optional
from datetime import datetime

from .interfaces import LecturaRepository
from ..domain.entities import Lectura
from ..domain.schemas import LecturaCreate, LecturaUpdate

class LecturaUseCases:
    """Casos de uso para operaciones de Lecturas"""
    
    def __init__(self, repository: LecturaRepository):
        self.repository = repository
    
    async def crear_lectura(self, lectura_data: LecturaCreate) -> Lectura:
        """Crea una nueva lectura"""
        # Validaciones de negocio adicionales si es necesario
        if lectura_data.valor < 0:
            raise ValueError("El valor de la lectura no puede ser negativo")
        
        return await self.repository.crear_lectura(lectura_data)
    
    async def obtener_lectura(self, id_lectura: int) -> Optional[Lectura]:
        """Obtiene una lectura por su ID"""
        if id_lectura <= 0:
            raise ValueError("El ID de la lectura debe ser un número positivo")
        
        return await self.repository.obtener_lectura(id_lectura)
    
    async def obtener_todas_lecturas(self) -> List[Lectura]:
        """Obtiene todas las lecturas"""
        return await self.repository.obtener_todas_lecturas()
    
    async def obtener_lecturas_por_sensor(self, id_sensor: int) -> List[Lectura]:
        """Obtiene todas las lecturas de un sensor específico"""
        if id_sensor <= 0:
            raise ValueError("El ID del sensor debe ser un número positivo")
        
        return await self.repository.obtener_lecturas_por_sensor(id_sensor)
    
    async def obtener_lecturas_por_rango_fechas(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Lectura]:
        """Obtiene lecturas dentro de un rango de fechas"""
        if fecha_inicio >= fecha_fin:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")
        
        return await self.repository.obtener_lecturas_por_rango_fechas(fecha_inicio, fecha_fin)
    
    async def obtener_lecturas_por_sensor_y_fechas(self, id_sensor: int, fecha_inicio: datetime, fecha_fin: datetime) -> List[Lectura]:
        """Obtiene lecturas de un sensor específico dentro de un rango de fechas"""
        if id_sensor <= 0:
            raise ValueError("El ID del sensor debe ser un número positivo")
        if fecha_inicio >= fecha_fin:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")
        
        return await self.repository.obtener_lecturas_por_sensor_y_fechas(id_sensor, fecha_inicio, fecha_fin)
    
    async def obtener_lecturas_criticas(self, limite_superior: float = 100.0, limite_inferior: float = 0.0) -> List[Lectura]:
        """Obtiene lecturas que están fuera de los límites normales"""
        if limite_inferior >= limite_superior:
            raise ValueError("El límite inferior debe ser menor que el límite superior")
        
        return await self.repository.obtener_lecturas_criticas(limite_superior, limite_inferior)
    
    async def obtener_ultimas_lecturas_por_sensor(self, id_sensor: int, limite: int = 10) -> List[Lectura]:
        """Obtiene las últimas N lecturas de un sensor específico"""
        if id_sensor <= 0:
            raise ValueError("El ID del sensor debe ser un número positivo")
        if limite <= 0:
            raise ValueError("El límite debe ser un número positivo")
        
        return await self.repository.obtener_ultimas_lecturas_por_sensor(id_sensor, limite)
    
    async def actualizar_lectura(self, id_lectura: int, lectura_data: LecturaUpdate) -> Optional[Lectura]:
        """Actualiza una lectura existente"""
        if id_lectura <= 0:
            raise ValueError("El ID de la lectura debe ser un número positivo")
        
        # Validaciones de negocio adicionales
        if lectura_data.valor is not None and lectura_data.valor < 0:
            raise ValueError("El valor de la lectura no puede ser negativo")
        
        if lectura_data.id_sensor is not None and lectura_data.id_sensor <= 0:
            raise ValueError("El ID del sensor debe ser un número positivo")
        
        return await self.repository.actualizar_lectura(id_lectura, lectura_data)
    
    async def eliminar_lectura(self, id_lectura: int) -> bool:
        """Elimina una lectura"""
        if id_lectura <= 0:
            raise ValueError("El ID de la lectura debe ser un número positivo")
        
        return await self.repository.eliminar_lectura(id_lectura)
    
    async def contar_lecturas_por_sensor(self, id_sensor: int) -> int:
        """Cuenta el número de lecturas de un sensor específico"""
        if id_sensor <= 0:
            raise ValueError("El ID del sensor debe ser un número positivo")
        
        return await self.repository.contar_lecturas_por_sensor(id_sensor)
    
    async def obtener_estadisticas_sensor(self, id_sensor: int) -> dict:
        """Obtiene estadísticas completas de un sensor"""
        if id_sensor <= 0:
            raise ValueError("El ID del sensor debe ser un número positivo")
        
        total_lecturas = await self.repository.contar_lecturas_por_sensor(id_sensor)
        valor_promedio = await self.repository.obtener_valor_promedio_por_sensor(id_sensor)
        min_max = await self.repository.obtener_valor_minimo_maximo_por_sensor(id_sensor)
        
        return {
            "id_sensor": id_sensor,
            "total_lecturas": total_lecturas,
            "valor_promedio": valor_promedio,
            "valor_minimo": min_max.get("minimo") if min_max else None,
            "valor_maximo": min_max.get("maximo") if min_max else None
        }
    
    async def analizar_tendencia_sensor(self, id_sensor: int, limite_lecturas: int = 100) -> dict:
        """Analiza la tendencia de las lecturas de un sensor"""
        if id_sensor <= 0:
            raise ValueError("El ID del sensor debe ser un número positivo")
        
        lecturas = await self.repository.obtener_ultimas_lecturas_por_sensor(id_sensor, limite_lecturas)
        
        if len(lecturas) < 2:
            return {
                "id_sensor": id_sensor,
                "tendencia": "insuficientes_datos",
                "total_lecturas": len(lecturas)
            }
        
        # Calcular tendencia simple (primera vs última lectura)
        primera_lectura = lecturas[-1]  # Las lecturas están ordenadas por fecha descendente
        ultima_lectura = lecturas[0]
        
        diferencia = ultima_lectura.valor - primera_lectura.valor
        porcentaje_cambio = (diferencia / primera_lectura.valor) * 100 if primera_lectura.valor != 0 else 0
        
        if abs(porcentaje_cambio) < 5:
            tendencia = "estable"
        elif porcentaje_cambio > 0:
            tendencia = "creciente"
        else:
            tendencia = "decreciente"
        
        return {
            "id_sensor": id_sensor,
            "tendencia": tendencia,
            "porcentaje_cambio": round(porcentaje_cambio, 2),
            "valor_inicial": primera_lectura.valor,
            "valor_final": ultima_lectura.valor,
            "total_lecturas": len(lecturas)
        }
