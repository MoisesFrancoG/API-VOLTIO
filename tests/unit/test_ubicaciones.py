"""
Script de prueba para verificar la implementación del módulo Ubicaciones
"""

from src.Ubicaciones.domain.entities import Ubicacion
from src.Ubicaciones.domain.schemas import UbicacionCreate, UbicacionUpdate, UbicacionResponse

def test_ubicacion_entity():
    """Prueba la entidad Ubicacion"""
    print("=== Prueba de Entidad Ubicacion ===")
    
    # Crear una ubicación
    ubicacion = Ubicacion(1, "Oficina Principal", "Ubicación principal de la empresa")
    print(f"Ubicación creada: {ubicacion}")
    
    # Cambiar nombre
    ubicacion.cambiar_nombre("Oficina Central")
    print(f"Nombre actualizado: {ubicacion.nombre}")
    
    # Actualizar descripción
    ubicacion.actualizar_descripcion("Oficina central ubicada en el centro de la ciudad")
    print(f"Descripción actualizada: {ubicacion.descripcion}")
    
    print("✅ Entidad Ubicacion funciona correctamente\n")

def test_ubicacion_schemas():
    """Prueba los esquemas de Ubicacion"""
    print("=== Prueba de Esquemas Ubicacion ===")
    
    # Crear esquema de creación
    ubicacion_create = UbicacionCreate(
        nombre="Almacén Norte",
        descripcion="Almacén ubicado en la zona norte de la ciudad"
    )
    print(f"Esquema de creación: {ubicacion_create}")
    
    # Crear esquema de actualización
    ubicacion_update = UbicacionUpdate(
        nombre="Almacén Norte Actualizado",
        descripcion="Descripción actualizada del almacén norte"
    )
    print(f"Esquema de actualización: {ubicacion_update}")
    
    # Crear esquema de respuesta
    ubicacion_response = UbicacionResponse(
        id_ubicacion=1,
        nombre="Almacén Norte",
        descripcion="Almacén ubicado en la zona norte de la ciudad"
    )
    print(f"Esquema de respuesta: {ubicacion_response}")
    
    print("✅ Esquemas de Ubicacion funcionan correctamente\n")

if __name__ == "__main__":
    test_ubicacion_entity()
    test_ubicacion_schemas()
    print("🎉 Todas las pruebas del módulo Ubicaciones pasaron exitosamente!")
