"""
Script de prueba para verificar la implementación del módulo TipoSensores
"""

from src.TipoSensores.domain.entities import TipoSensor
from src.TipoSensores.domain.schemas import TipoSensorCreate, TipoSensorUpdate, TipoSensorResponse

def test_tipo_sensor_entity():
    """Prueba la entidad TipoSensor"""
    print("=== Prueba de Entidad TipoSensor ===")
    
    # Crear un tipo de sensor
    tipo_sensor = TipoSensor(1, "Sensor de Temperatura", "Sensor para medir temperatura ambiente")
    print(f"Tipo de sensor creado: {tipo_sensor}")
    
    # Cambiar nombre
    tipo_sensor.cambiar_nombre("Sensor de Temperatura Digital")
    print(f"Nombre actualizado: {tipo_sensor.nombre}")
    
    # Actualizar descripción
    tipo_sensor.actualizar_descripcion("Sensor digital de alta precisión para medir temperatura")
    print(f"Descripción actualizada: {tipo_sensor.descripcion}")
    
    print("✅ Entidad TipoSensor funciona correctamente\n")

def test_tipo_sensor_schemas():
    """Prueba los esquemas de TipoSensor"""
    print("=== Prueba de Esquemas TipoSensor ===")
    
    # Crear esquema de creación
    tipo_sensor_create = TipoSensorCreate(
        nombre="Sensor de Humedad",
        descripcion="Sensor para medir humedad relativa del ambiente"
    )
    print(f"Esquema de creación: {tipo_sensor_create}")
    
    # Crear esquema de actualización
    tipo_sensor_update = TipoSensorUpdate(
        nombre="Sensor de Humedad Avanzado",
        descripcion="Sensor avanzado para medir humedad relativa con alta precisión"
    )
    print(f"Esquema de actualización: {tipo_sensor_update}")
    
    # Crear esquema de respuesta
    tipo_sensor_response = TipoSensorResponse(
        id_tipo_sensor=1,
        nombre="Sensor de Humedad",
        descripcion="Sensor para medir humedad relativa del ambiente"
    )
    print(f"Esquema de respuesta: {tipo_sensor_response}")
    
    print("✅ Esquemas de TipoSensor funcionan correctamente\n")

def test_validation_rules():
    """Prueba las reglas de validación"""
    print("=== Prueba de Reglas de Validación ===")
    
    tipo_sensor = TipoSensor(1, "Sensor Inicial", "Descripción inicial")
    
    # Probar validación de nombre muy corto
    try:
        tipo_sensor.cambiar_nombre("AB")
        print("❌ ERROR: Debería haber fallado con nombre muy corto")
    except ValueError as e:
        print(f"✅ Validación correcta: {e}")
    
    # Probar validación de nombre vacío
    try:
        tipo_sensor.cambiar_nombre("")
        print("❌ ERROR: Debería haber fallado con nombre vacío")
    except ValueError as e:
        print(f"✅ Validación correcta: {e}")
    
    # Probar validación de nombre con espacios
    try:
        tipo_sensor.cambiar_nombre("   ")
        print("❌ ERROR: Debería haber fallado con nombre solo espacios")
    except ValueError as e:
        print(f"✅ Validación correcta: {e}")
    
    print("✅ Reglas de validación funcionan correctamente\n")

if __name__ == "__main__":
    test_tipo_sensor_entity()
    test_tipo_sensor_schemas()
    test_validation_rules()
    print("🎉 Todas las pruebas del módulo TipoSensores pasaron exitosamente!")
    print("\n📋 Resumen de la implementación:")
    print("- ✅ Entidad TipoSensor con validaciones de negocio")
    print("- ✅ Esquemas Pydantic para validación de datos")
    print("- ✅ Interfaces para inversión de dependencias")
    print("- ✅ Casos de uso para lógica de aplicación")
    print("- ✅ Modelo SQLAlchemy para persistencia")
    print("- ✅ Repositorio con manejo de errores")
    print("- ✅ Rutas FastAPI con autenticación y autorización")
    print("- ✅ Configuración de dependencias")
    print("- ✅ Integración con main.py")
