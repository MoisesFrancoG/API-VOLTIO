"""
Casos de uso para el módulo de Sensores
"""

from typing import List, Optional

from .interfaces import SensorRepository
from ..domain.entities import Sensor
from ..domain.schemas import SensorCreate, SensorUpdate

class SensorUseCases:
    """Casos de uso para operaciones de Sensores"""
    
    def __init__(self, repository: SensorRepository):
        self.repository = repository
    
    def crear_sensor(self, sensor_data: SensorCreate) -> Sensor:
        """Crea un nuevo sensor"""
        # Validar que el nombre no esté duplicado
        if self.repository.existe_sensor_con_nombre(sensor_data.nombre):
            raise ValueError(f"Ya existe un sensor con el nombre '{sensor_data.nombre}'")
        
        # Validaciones adicionales de negocio
        if sensor_data.id_tipo_sensor <= 0:
            raise ValueError("El ID del tipo de sensor debe ser un número positivo")
        
        if sensor_data.id_ubicacion <= 0:
            raise ValueError("El ID de la ubicación debe ser un número positivo")
        
        if sensor_data.id_usuario <= 0:
            raise ValueError("El ID del usuario debe ser un número positivo")
        
        return self.repository.crear_sensor(sensor_data)
    
    def obtener_sensor(self, id_sensor: int) -> Optional[Sensor]:
        """Obtiene un sensor por su ID"""
        if id_sensor <= 0:
            raise ValueError("El ID del sensor debe ser un número positivo")
        
        return self.repository.obtener_sensor(id_sensor)
    
    def obtener_todos_sensores(self) -> List[Sensor]:
        """Obtiene todos los sensores"""
        return self.repository.obtener_todos_sensores()
    
    def obtener_sensores_activos(self) -> List[Sensor]:
        """Obtiene solo los sensores activos"""
        return self.repository.obtener_sensores_activos()
    
    def obtener_sensores_por_tipo(self, id_tipo_sensor: int) -> List[Sensor]:
        """Obtiene sensores por tipo"""
        if id_tipo_sensor <= 0:
            raise ValueError("El ID del tipo de sensor debe ser un número positivo")
        
        return self.repository.obtener_sensores_por_tipo(id_tipo_sensor)
    
    def obtener_sensores_por_ubicacion(self, id_ubicacion: int) -> List[Sensor]:
        """Obtiene sensores por ubicación"""
        if id_ubicacion <= 0:
            raise ValueError("El ID de la ubicación debe ser un número positivo")
        
        return self.repository.obtener_sensores_por_ubicacion(id_ubicacion)
    
    def obtener_sensores_por_usuario(self, id_usuario: int) -> List[Sensor]:
        """Obtiene sensores por usuario"""
        if id_usuario <= 0:
            raise ValueError("El ID del usuario debe ser un número positivo")
        
        return self.repository.obtener_sensores_por_usuario(id_usuario)
    
    def buscar_sensores_por_nombre(self, nombre: str) -> List[Sensor]:
        """Busca sensores por nombre"""
        if not nombre or len(nombre.strip()) < 2:
            raise ValueError("El término de búsqueda debe tener al menos 2 caracteres")
        
        return self.repository.buscar_sensores_por_nombre(nombre.strip())
    
    def actualizar_sensor(self, id_sensor: int, sensor_data: SensorUpdate) -> Optional[Sensor]:
        """Actualiza un sensor existente"""
        if id_sensor <= 0:
            raise ValueError("El ID del sensor debe ser un número positivo")
        
        # Validar que el sensor existe
        sensor_existente = self.repository.obtener_sensor(id_sensor)
        if not sensor_existente:
            return None
        
        # Validar nombre único si se está cambiando
        if sensor_data.nombre and sensor_data.nombre != sensor_existente.nombre:
            if self.repository.existe_sensor_con_nombre(sensor_data.nombre, id_sensor):
                raise ValueError(f"Ya existe otro sensor con el nombre '{sensor_data.nombre}'")
        
        # Validaciones adicionales
        if sensor_data.id_tipo_sensor is not None and sensor_data.id_tipo_sensor <= 0:
            raise ValueError("El ID del tipo de sensor debe ser un número positivo")
        
        if sensor_data.id_ubicacion is not None and sensor_data.id_ubicacion <= 0:
            raise ValueError("El ID de la ubicación debe ser un número positivo")
        
        if sensor_data.id_usuario is not None and sensor_data.id_usuario <= 0:
            raise ValueError("El ID del usuario debe ser un número positivo")
        
        return self.repository.actualizar_sensor(id_sensor, sensor_data)
    
    def cambiar_estado_sensor(self, id_sensor: int, activo: bool) -> Optional[Sensor]:
        """Cambia solo el estado activo/inactivo del sensor"""
        if id_sensor <= 0:
            raise ValueError("El ID del sensor debe ser un número positivo")
        
        sensor_existente = self.repository.obtener_sensor(id_sensor)
        if not sensor_existente:
            return None
        
        if sensor_existente.activo == activo:
            raise ValueError(f"El sensor ya está {'activo' if activo else 'inactivo'}")
        
        return self.repository.cambiar_estado_sensor(id_sensor, activo)
    
    def eliminar_sensor(self, id_sensor: int) -> bool:
        """Elimina un sensor"""
        if id_sensor <= 0:
            raise ValueError("El ID del sensor debe ser un número positivo")
        
        return self.repository.eliminar_sensor(id_sensor)
    
    def obtener_estadisticas_por_tipo(self, id_tipo_sensor: int) -> dict:
        """Obtiene estadísticas de sensores por tipo"""
        if id_tipo_sensor <= 0:
            raise ValueError("El ID del tipo de sensor debe ser un número positivo")
        
        total_sensores = self.repository.contar_sensores_por_tipo(id_tipo_sensor)
        sensores_del_tipo = self.repository.obtener_sensores_por_tipo(id_tipo_sensor)
        sensores_activos = len([s for s in sensores_del_tipo if s.activo])
        sensores_inactivos = total_sensores - sensores_activos
        
        return {
            "id_tipo_sensor": id_tipo_sensor,
            "total_sensores": total_sensores,
            "sensores_activos": sensores_activos,
            "sensores_inactivos": sensores_inactivos,
            "porcentaje_activos": round((sensores_activos / total_sensores) * 100, 2) if total_sensores > 0 else 0
        }
    
    def obtener_estadisticas_por_ubicacion(self, id_ubicacion: int) -> dict:
        """Obtiene estadísticas de sensores por ubicación"""
        if id_ubicacion <= 0:
            raise ValueError("El ID de la ubicación debe ser un número positivo")
        
        total_sensores = self.repository.contar_sensores_por_ubicacion(id_ubicacion)
        sensores_de_ubicacion = self.repository.obtener_sensores_por_ubicacion(id_ubicacion)
        sensores_activos = len([s for s in sensores_de_ubicacion if s.activo])
        sensores_inactivos = total_sensores - sensores_activos
        
        return {
            "id_ubicacion": id_ubicacion,
            "total_sensores": total_sensores,
            "sensores_activos": sensores_activos,
            "sensores_inactivos": sensores_inactivos,
            "porcentaje_activos": round((sensores_activos / total_sensores) * 100, 2) if total_sensores > 0 else 0
        }
    
    def obtener_estadisticas_por_usuario(self, id_usuario: int) -> dict:
        """Obtiene estadísticas de sensores por usuario"""
        if id_usuario <= 0:
            raise ValueError("El ID del usuario debe ser un número positivo")
        
        total_sensores = self.repository.contar_sensores_por_usuario(id_usuario)
        sensores_del_usuario = self.repository.obtener_sensores_por_usuario(id_usuario)
        sensores_activos = len([s for s in sensores_del_usuario if s.activo])
        sensores_inactivos = total_sensores - sensores_activos
        
        return {
            "id_usuario": id_usuario,
            "total_sensores": total_sensores,
            "sensores_activos": sensores_activos,
            "sensores_inactivos": sensores_inactivos,
            "porcentaje_activos": round((sensores_activos / total_sensores) * 100, 2) if total_sensores > 0 else 0
        }
    
    def validar_configuracion_sensor(self, id_sensor: int) -> dict:
        """Valida la configuración de un sensor"""
        if id_sensor <= 0:
            raise ValueError("El ID del sensor debe ser un número positivo")
        
        sensor = self.repository.obtener_sensor(id_sensor)
        if not sensor:
            raise ValueError("Sensor no encontrado")
        
        # Crear entidad de dominio para validar
        sensor_entidad = Sensor(
            id_sensor=sensor.id_sensor,
            nombre=sensor.nombre,
            id_tipo_sensor=sensor.id_tipo_sensor,
            id_ubicacion=sensor.id_ubicacion,
            id_usuario=sensor.id_usuario,
            activo=sensor.activo
        )
        
        configuracion_valida = sensor_entidad.validar_configuracion()
        puede_generar_lecturas = sensor_entidad.puede_generar_lecturas()
        
        return {
            "id_sensor": id_sensor,
            "configuracion_valida": configuracion_valida,
            "puede_generar_lecturas": puede_generar_lecturas,
            "esta_activo": sensor_entidad.esta_activo(),
            "validaciones": {
                "nombre_valido": len(sensor.nombre.strip()) >= 3,
                "tipo_sensor_valido": sensor.id_tipo_sensor > 0,
                "ubicacion_valida": sensor.id_ubicacion > 0,
                "usuario_valido": sensor.id_usuario > 0
            }
        }
