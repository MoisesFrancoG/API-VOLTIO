"""
Script de prueba para el módulo de Sensores
"""

import asyncio
import httpx
from datetime import datetime

# Configuración del cliente HTTP
BASE_URL = "http://localhost:8000/api/v1/sensores"

async def test_sensores_crud():
    """Test completo de CRUD para Sensores"""
    
    async with httpx.AsyncClient() as client:
        print("=== PRUEBAS DEL MÓDULO DE SENSORES ===\n")
        
        # 1. Crear varios sensores de prueba
        print("1. Creando sensores de prueba...")
        
        sensores_prueba = [
            {
                "nombre": "Sensor Temperatura Sala 1",
                "id_tipo_sensor": 1,
                "id_ubicacion": 1,
                "id_usuario": 1,
                "activo": True
            },
            {
                "nombre": "Sensor Humedad Sala 1",
                "id_tipo_sensor": 2,
                "id_ubicacion": 1,
                "id_usuario": 1,
                "activo": True
            },
            {
                "nombre": "Sensor Presencia Sala 2",
                "id_tipo_sensor": 3,
                "id_ubicacion": 2,
                "id_usuario": 2,
                "activo": False
            },
            {
                "nombre": "Sensor Temperatura Exterior",
                "id_tipo_sensor": 1,
                "id_ubicacion": 3,
                "id_usuario": 1,
                "activo": True
            }
        ]
        
        sensores_creados = []
        for sensor_data in sensores_prueba:
            response = await client.post(BASE_URL, json=sensor_data)
            if response.status_code == 200:
                sensor = response.json()
                sensores_creados.append(sensor)
                estado = "Activo" if sensor['activo'] else "Inactivo"
                print(f"✓ Sensor creado: ID {sensor['id_sensor']}, Nombre: {sensor['nombre']}, Estado: {estado}")
            else:
                print(f"✗ Error al crear sensor: {response.status_code} - {response.text}")
        
        if not sensores_creados:
            print("No se pudieron crear sensores de prueba.")
            return
        
        # 2. Obtener todos los sensores
        print("\n2. Obteniendo todos los sensores...")
        response = await client.get(BASE_URL)
        if response.status_code == 200:
            sensores = response.json()
            print(f"✓ Total de sensores encontrados: {len(sensores)}")
            for sensor in sensores:
                estado = "Activo" if sensor['activo'] else "Inactivo"
                print(f"  - ID: {sensor['id_sensor']}, Nombre: {sensor['nombre']}, Estado: {estado}")
        else:
            print(f"✗ Error al obtener sensores: {response.status_code}")
        
        # 3. Obtener sensor específico
        print("\n3. Obteniendo sensor específico...")
        sensor_id = sensores_creados[0]['id_sensor']
        response = await client.get(f"{BASE_URL}/{sensor_id}")
        if response.status_code == 200:
            sensor = response.json()
            print(f"✓ Sensor encontrado: ID {sensor['id_sensor']}, Nombre: {sensor['nombre']}")
        else:
            print(f"✗ Error al obtener sensor: {response.status_code}")
        
        # 4. Obtener sensores activos
        print("\n4. Obteniendo sensores activos...")
        response = await client.get(f"{BASE_URL}/activos/")
        if response.status_code == 200:
            sensores_activos = response.json()
            print(f"✓ Sensores activos: {len(sensores_activos)}")
            for sensor in sensores_activos:
                print(f"  - ID: {sensor['id_sensor']}, Nombre: {sensor['nombre']}")
        else:
            print(f"✗ Error al obtener sensores activos: {response.status_code}")
        
        # 5. Obtener sensores por tipo
        print("\n5. Obteniendo sensores por tipo...")
        id_tipo = 1  # Tipo temperatura
        response = await client.get(f"{BASE_URL}/tipo/{id_tipo}")
        if response.status_code == 200:
            sensores_tipo = response.json()
            print(f"✓ Sensores del tipo {id_tipo}: {len(sensores_tipo)}")
            for sensor in sensores_tipo:
                print(f"  - ID: {sensor['id_sensor']}, Nombre: {sensor['nombre']}")
        else:
            print(f"✗ Error al obtener sensores por tipo: {response.status_code}")
        
        # 6. Obtener sensores por ubicación
        print("\n6. Obteniendo sensores por ubicación...")
        id_ubicacion = 1
        response = await client.get(f"{BASE_URL}/ubicacion/{id_ubicacion}")
        if response.status_code == 200:
            sensores_ubicacion = response.json()
            print(f"✓ Sensores en ubicación {id_ubicacion}: {len(sensores_ubicacion)}")
            for sensor in sensores_ubicacion:
                print(f"  - ID: {sensor['id_sensor']}, Nombre: {sensor['nombre']}")
        else:
            print(f"✗ Error al obtener sensores por ubicación: {response.status_code}")
        
        # 7. Obtener sensores por usuario
        print("\n7. Obteniendo sensores por usuario...")
        id_usuario = 1
        response = await client.get(f"{BASE_URL}/usuario/{id_usuario}")
        if response.status_code == 200:
            sensores_usuario = response.json()
            print(f"✓ Sensores del usuario {id_usuario}: {len(sensores_usuario)}")
            for sensor in sensores_usuario:
                print(f"  - ID: {sensor['id_sensor']}, Nombre: {sensor['nombre']}")
        else:
            print(f"✗ Error al obtener sensores por usuario: {response.status_code}")
        
        # 8. Buscar sensores por nombre
        print("\n8. Buscando sensores por nombre...")
        termino_busqueda = "Temperatura"
        response = await client.get(f"{BASE_URL}/buscar/?nombre={termino_busqueda}")
        if response.status_code == 200:
            sensores_encontrados = response.json()
            print(f"✓ Sensores encontrados con '{termino_busqueda}': {len(sensores_encontrados)}")
            for sensor in sensores_encontrados:
                print(f"  - ID: {sensor['id_sensor']}, Nombre: {sensor['nombre']}")
        else:
            print(f"✗ Error al buscar sensores: {response.status_code}")
        
        # 9. Obtener estadísticas por tipo
        print("\n9. Obteniendo estadísticas por tipo...")
        response = await client.get(f"{BASE_URL}/tipo/{id_tipo}/estadisticas")
        if response.status_code == 200:
            estadisticas = response.json()
            print(f"✓ Estadísticas del tipo {id_tipo}:")
            print(f"  - Total sensores: {estadisticas['total_sensores']}")
            print(f"  - Sensores activos: {estadisticas['sensores_activos']}")
            print(f"  - Sensores inactivos: {estadisticas['sensores_inactivos']}")
            print(f"  - Porcentaje activos: {estadisticas['porcentaje_activos']}%")
        else:
            print(f"✗ Error al obtener estadísticas por tipo: {response.status_code}")
        
        # 10. Obtener estadísticas por ubicación
        print("\n10. Obteniendo estadísticas por ubicación...")
        response = await client.get(f"{BASE_URL}/ubicacion/{id_ubicacion}/estadisticas")
        if response.status_code == 200:
            estadisticas = response.json()
            print(f"✓ Estadísticas de ubicación {id_ubicacion}:")
            print(f"  - Total sensores: {estadisticas['total_sensores']}")
            print(f"  - Sensores activos: {estadisticas['sensores_activos']}")
            print(f"  - Sensores inactivos: {estadisticas['sensores_inactivos']}")
            print(f"  - Porcentaje activos: {estadisticas['porcentaje_activos']}%")
        else:
            print(f"✗ Error al obtener estadísticas por ubicación: {response.status_code}")
        
        # 11. Validar configuración de sensor
        print("\n11. Validando configuración de sensor...")
        sensor_id = sensores_creados[0]['id_sensor']
        response = await client.get(f"{BASE_URL}/{sensor_id}/validar")
        if response.status_code == 200:
            validacion = response.json()
            print(f"✓ Validación del sensor {sensor_id}:")
            print(f"  - Configuración válida: {validacion['configuracion_valida']}")
            print(f"  - Puede generar lecturas: {validacion['puede_generar_lecturas']}")
            print(f"  - Está activo: {validacion['esta_activo']}")
        else:
            print(f"✗ Error al validar configuración: {response.status_code}")
        
        # 12. Cambiar estado de sensor
        print("\n12. Cambiando estado de sensor...")
        sensor_id = sensores_creados[0]['id_sensor']
        nuevo_estado = {"activo": False}
        response = await client.patch(f"{BASE_URL}/{sensor_id}/estado", json=nuevo_estado)
        if response.status_code == 200:
            sensor_actualizado = response.json()
            estado = "Activo" if sensor_actualizado['activo'] else "Inactivo"
            print(f"✓ Estado cambiado: ID {sensor_actualizado['id_sensor']}, Nuevo estado: {estado}")
        else:
            print(f"✗ Error al cambiar estado: {response.status_code}")
        
        # 13. Actualizar sensor
        print("\n13. Actualizando sensor...")
        sensor_id = sensores_creados[1]['id_sensor']
        datos_actualizacion = {
            "nombre": "Sensor Humedad Actualizado",
            "activo": True
        }
        response = await client.put(f"{BASE_URL}/{sensor_id}", json=datos_actualizacion)
        if response.status_code == 200:
            sensor_actualizado = response.json()
            print(f"✓ Sensor actualizado: ID {sensor_actualizado['id_sensor']}, Nombre: {sensor_actualizado['nombre']}")
        else:
            print(f"✗ Error al actualizar sensor: {response.status_code}")
        
        # 14. Eliminar sensor
        print("\n14. Eliminando sensor...")
        sensor_id = sensores_creados[-1]['id_sensor']
        response = await client.delete(f"{BASE_URL}/{sensor_id}")
        if response.status_code == 200:
            print(f"✓ Sensor eliminado: ID {sensor_id}")
        else:
            print(f"✗ Error al eliminar sensor: {response.status_code}")
        
        print("\n=== PRUEBAS COMPLETADAS ===")

async def test_validaciones():
    """Test de validaciones específicas"""
    
    async with httpx.AsyncClient() as client:
        print("\n=== PRUEBAS DE VALIDACIÓN ===\n")
        
        # Nombre muy corto
        print("1. Probando nombre muy corto...")
        response = await client.post(BASE_URL, json={
            "nombre": "AB",
            "id_tipo_sensor": 1,
            "id_ubicacion": 1,
            "id_usuario": 1,
            "activo": True
        })
        if response.status_code == 400:
            print("✓ Validación de nombre corto funcionando")
        else:
            print(f"✗ Error en validación de nombre corto: {response.status_code}")
        
        # ID tipo sensor inválido
        print("2. Probando ID tipo sensor inválido...")
        response = await client.post(BASE_URL, json={
            "nombre": "Sensor Válido",
            "id_tipo_sensor": 0,
            "id_ubicacion": 1,
            "id_usuario": 1,
            "activo": True
        })
        if response.status_code == 400:
            print("✓ Validación de ID tipo sensor inválido funcionando")
        else:
            print(f"✗ Error en validación de ID tipo sensor: {response.status_code}")
        
        # ID ubicación inválido
        print("3. Probando ID ubicación inválido...")
        response = await client.post(BASE_URL, json={
            "nombre": "Sensor Válido",
            "id_tipo_sensor": 1,
            "id_ubicacion": -1,
            "id_usuario": 1,
            "activo": True
        })
        if response.status_code == 400:
            print("✓ Validación de ID ubicación inválido funcionando")
        else:
            print(f"✗ Error en validación de ID ubicación: {response.status_code}")
        
        print("\n=== PRUEBAS DE VALIDACIÓN COMPLETADAS ===")

def main():
    """Función principal para ejecutar las pruebas"""
    print("Iniciando pruebas del módulo de Sensores...")
    print("Asegúrate de que la API esté corriendo en http://localhost:8000")
    input("Presiona Enter para continuar...")
    
    asyncio.run(test_sensores_crud())
    asyncio.run(test_validaciones())

if __name__ == "__main__":
    main()
