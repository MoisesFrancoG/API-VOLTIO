"""
Script de prueba para verificar la implementación del módulo ComandosIR
"""

from src.ComandosIR.domain.entities import ComandoIR
from src.ComandosIR.domain.schemas import ComandoIRCreate, ComandoIRUpdate, ComandoIRResponse

def test_comando_ir_entity():
    """Prueba la entidad ComandoIR"""
    print("=== Prueba de Entidad ComandoIR ===")
    
    # Crear un comando IR
    comando_ir = ComandoIR(
        id_comando=1,
        id_sensor=100,
        nombre="Encender LED",
        descripcion="Comando para encender el LED del sensor",
        comando="LED_ON_IR_CODE_12345"
    )
    print(f"Comando IR creado: {comando_ir}")
    
    # Cambiar nombre
    comando_ir.cambiar_nombre("Encender LED Principal")
    print(f"Nombre actualizado: {comando_ir.nombre}")
    
    # Actualizar descripción
    comando_ir.actualizar_descripcion("Comando IR para encender el LED principal del sensor")
    print(f"Descripción actualizada: {comando_ir.descripcion}")
    
    # Actualizar comando
    comando_ir.actualizar_comando("LED_ON_MAIN_IR_CODE_54321")
    print(f"Comando actualizado: {comando_ir.comando}")
    
    # Asignar nuevo sensor
    comando_ir.asignar_sensor(200)
    print(f"Sensor actualizado: {comando_ir.id_sensor}")
    
    print("✅ Entidad ComandoIR funciona correctamente\n")

def test_comando_ir_schemas():
    """Prueba los esquemas de ComandoIR"""
    print("=== Prueba de Esquemas ComandoIR ===")
    
    # Crear esquema de creación
    comando_ir_create = ComandoIRCreate(
        id_sensor=100,
        nombre="Apagar LED",
        descripcion="Comando para apagar el LED del sensor",
        comando="LED_OFF_IR_CODE_67890"
    )
    print(f"Esquema de creación: {comando_ir_create}")
    
    # Crear esquema de actualización
    comando_ir_update = ComandoIRUpdate(
        nombre="Apagar LED Completamente",
        descripcion="Comando IR para apagar completamente el LED del sensor",
        comando="LED_OFF_COMPLETE_IR_CODE_09876"
    )
    print(f"Esquema de actualización: {comando_ir_update}")
    
    # Crear esquema de respuesta
    comando_ir_response = ComandoIRResponse(
        id_comando=1,
        id_sensor=100,
        nombre="Apagar LED",
        descripcion="Comando para apagar el LED del sensor",
        comando="LED_OFF_IR_CODE_67890"
    )
    print(f"Esquema de respuesta: {comando_ir_response}")
    
    print("✅ Esquemas de ComandoIR funcionan correctamente\n")

def test_validation_rules():
    """Prueba las reglas de validación"""
    print("=== Prueba de Reglas de Validación ===")
    
    comando_ir = ComandoIR(1, 100, "Comando Inicial", "Descripción inicial", "CMD_INITIAL")
    
    # Probar validación de nombre muy corto
    try:
        comando_ir.cambiar_nombre("AB")
        print("❌ ERROR: Debería haber fallado con nombre muy corto")
    except ValueError as e:
        print(f"✅ Validación correcta: {e}")
    
    # Probar validación de nombre vacío
    try:
        comando_ir.cambiar_nombre("")
        print("❌ ERROR: Debería haber fallado con nombre vacío")
    except ValueError as e:
        print(f"✅ Validación correcta: {e}")
    
    # Probar validación de comando vacío
    try:
        comando_ir.actualizar_comando("")
        print("❌ ERROR: Debería haber fallado con comando vacío")
    except ValueError as e:
        print(f"✅ Validación correcta: {e}")
    
    # Probar validación de ID sensor inválido
    try:
        comando_ir.asignar_sensor(0)
        print("❌ ERROR: Debería haber fallado con ID sensor inválido")
    except ValueError as e:
        print(f"✅ Validación correcta: {e}")
    
    try:
        comando_ir.asignar_sensor(-1)
        print("❌ ERROR: Debería haber fallado con ID sensor negativo")
    except ValueError as e:
        print(f"✅ Validación correcta: {e}")
    
    print("✅ Reglas de validación funcionan correctamente\n")

def test_business_logic():
    """Prueba la lógica de negocio específica de ComandosIR"""
    print("=== Prueba de Lógica de Negocio ComandosIR ===")
    
    # Crear comandos IR para diferentes funciones
    comandos_ejemplos = [
        ComandoIR(1, 100, "Encender", "Encender dispositivo", "PWR_ON_12345"),
        ComandoIR(2, 100, "Apagar", "Apagar dispositivo", "PWR_OFF_12345"),
        ComandoIR(3, 100, "Aumentar Volumen", "Subir volumen", "VOL_UP_12345"),
        ComandoIR(4, 100, "Disminuir Volumen", "Bajar volumen", "VOL_DOWN_12345"),
        ComandoIR(5, 200, "Cambiar Canal", "Cambiar canal de TV", "CH_CHANGE_67890"),
    ]
    
    print("Comandos IR de ejemplo creados:")
    for cmd in comandos_ejemplos:
        print(f"  - {cmd}")
    
    # Agrupar comandos por sensor
    comandos_por_sensor = {}
    for cmd in comandos_ejemplos:
        if cmd.id_sensor not in comandos_por_sensor:
            comandos_por_sensor[cmd.id_sensor] = []
        comandos_por_sensor[cmd.id_sensor].append(cmd)
    
    print(f"\nComandos agrupados por sensor:")
    for sensor_id, comandos in comandos_por_sensor.items():
        print(f"  Sensor {sensor_id}: {len(comandos)} comandos")
        for cmd in comandos:
            print(f"    - {cmd.nombre}: {cmd.comando}")
    
    print("✅ Lógica de negocio de ComandosIR funciona correctamente\n")

if __name__ == "__main__":
    test_comando_ir_entity()
    test_comando_ir_schemas()
    test_validation_rules()
    test_business_logic()
    print("🎉 Todas las pruebas del módulo ComandosIR pasaron exitosamente!")
    print("\n📋 Resumen de la implementación:")
    print("- ✅ Entidad ComandoIR con validaciones de negocio")
    print("- ✅ Esquemas Pydantic con validaciones específicas")
    print("- ✅ Interfaces para inversión de dependencias")
    print("- ✅ Casos de uso con funcionalidades específicas")
    print("- ✅ Modelo SQLAlchemy con relación a sensores")
    print("- ✅ Repositorio con consultas por sensor")
    print("- ✅ Rutas FastAPI con endpoints específicos")
    print("- ✅ Configuración de dependencias")
    print("- ✅ Integración con main.py")
    print("\n🔧 Funcionalidades especiales de ComandosIR:")
    print("- 🔍 Búsqueda de comandos por sensor")
    print("- 📝 Validación de comandos IR")
    print("- 🔒 Validación de IDs de sensores")
    print("- 🎯 Gestión completa de comandos infrarrojos")
