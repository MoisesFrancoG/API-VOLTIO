"""
Script de prueba para el módulo de Lecturas
"""

import asyncio
import httpx
from datetime import datetime, timedelta

# Configuración del cliente HTTP
BASE_URL = "http://localhost:8000/api/v1/lecturas"

async def test_lecturas_crud():
    """Test completo de CRUD para Lecturas"""
    
    async with httpx.AsyncClient() as client:
        print("=== PRUEBAS DEL MÓDULO DE LECTURAS ===\n")
        
        # 1. Crear varias lecturas de prueba
        print("1. Creando lecturas de prueba...")
        
        lecturas_prueba = [
            {
                "id_sensor": 1,
                "valor": 25.5,
                "unidad": "°C",
                "fecha_hora": (datetime.now() - timedelta(hours=1)).isoformat()
            },
            {
                "id_sensor": 1,
                "valor": 26.2,
                "unidad": "°C",
                "fecha_hora": (datetime.now() - timedelta(minutes=30)).isoformat()
            },
            {
                "id_sensor": 1,
                "valor": 24.8,
                "unidad": "°C",
                "fecha_hora": datetime.now().isoformat()
            },
            {
                "id_sensor": 2,
                "valor": 220.5,
                "unidad": "V",
                "fecha_hora": (datetime.now() - timedelta(minutes=45)).isoformat()
            },
            {
                "id_sensor": 2,
                "valor": 225.0,
                "unidad": "V",
                "fecha_hora": datetime.now().isoformat()
            },
            {
                "id_sensor": 3,
                "valor": 15.5,
                "unidad": "A",
                "fecha_hora": datetime.now().isoformat()
            },
            {
                "id_sensor": 3,
                "valor": 150.0,  # Valor crítico alto
                "unidad": "A",
                "fecha_hora": datetime.now().isoformat()
            }
        ]
        
        lecturas_creadas = []
        for lectura_data in lecturas_prueba:
            response = await client.post(BASE_URL, json=lectura_data)
            if response.status_code == 200:
                lectura = response.json()
                lecturas_creadas.append(lectura)
                print(f"✓ Lectura creada: ID {lectura['id_lectura']}, Sensor {lectura['id_sensor']}, Valor: {lectura['valor']}{lectura['unidad']}")
            else:
                print(f"✗ Error al crear lectura: {response.status_code} - {response.text}")
        
        if not lecturas_creadas:
            print("No se pudieron crear lecturas de prueba.")
            return
        
        # 2. Obtener todas las lecturas
        print("\n2. Obteniendo todas las lecturas...")
        response = await client.get(BASE_URL)
        if response.status_code == 200:
            lecturas = response.json()
            print(f"✓ Total de lecturas encontradas: {len(lecturas)}")
            for lectura in lecturas[:5]:  # Mostrar solo las primeras 5
                print(f"  - ID: {lectura['id_lectura']}, Sensor: {lectura['id_sensor']}, Valor: {lectura['valor']}{lectura['unidad']}")
        else:
            print(f"✗ Error al obtener lecturas: {response.status_code}")
        
        # 3. Obtener lectura específica
        print("\n3. Obteniendo lectura específica...")
        lectura_id = lecturas_creadas[0]['id_lectura']
        response = await client.get(f"{BASE_URL}/{lectura_id}")
        if response.status_code == 200:
            lectura = response.json()
            print(f"✓ Lectura encontrada: ID {lectura['id_lectura']}, Valor: {lectura['valor']}{lectura['unidad']}")
        else:
            print(f"✗ Error al obtener lectura: {response.status_code}")
        
        # 4. Obtener lecturas por sensor
        print("\n4. Obteniendo lecturas por sensor...")
        id_sensor = 1
        response = await client.get(f"{BASE_URL}/sensor/{id_sensor}")
        if response.status_code == 200:
            lecturas_sensor = response.json()
            print(f"✓ Lecturas del sensor {id_sensor}: {len(lecturas_sensor)}")
            for lectura in lecturas_sensor:
                print(f"  - ID: {lectura['id_lectura']}, Valor: {lectura['valor']}{lectura['unidad']}, Fecha: {lectura['fecha_hora']}")
        else:
            print(f"✗ Error al obtener lecturas por sensor: {response.status_code}")
        
        # 5. Obtener últimas lecturas por sensor
        print("\n5. Obteniendo últimas lecturas por sensor...")
        response = await client.get(f"{BASE_URL}/sensor/{id_sensor}/ultimas?limite=2")
        if response.status_code == 200:
            ultimas_lecturas = response.json()
            print(f"✓ Últimas {len(ultimas_lecturas)} lecturas del sensor {id_sensor}:")
            for lectura in ultimas_lecturas:
                print(f"  - ID: {lectura['id_lectura']}, Valor: {lectura['valor']}{lectura['unidad']}, Fecha: {lectura['fecha_hora']}")
        else:
            print(f"✗ Error al obtener últimas lecturas: {response.status_code}")
        
        # 6. Obtener lecturas críticas
        print("\n6. Obteniendo lecturas críticas...")
        response = await client.get(f"{BASE_URL}/criticas/?limite_superior=100&limite_inferior=0")
        if response.status_code == 200:
            lecturas_criticas = response.json()
            print(f"✓ Lecturas críticas encontradas: {len(lecturas_criticas)}")
            for lectura in lecturas_criticas:
                print(f"  - ID: {lectura['id_lectura']}, Sensor: {lectura['id_sensor']}, Valor: {lectura['valor']}{lectura['unidad']} (CRÍTICO)")
        else:
            print(f"✗ Error al obtener lecturas críticas: {response.status_code}")
        
        # 7. Obtener estadísticas por sensor
        print("\n7. Obteniendo estadísticas por sensor...")
        response = await client.get(f"{BASE_URL}/sensor/{id_sensor}/estadisticas")
        if response.status_code == 200:
            estadisticas = response.json()
            print(f"✓ Estadísticas del sensor {id_sensor}:")
            print(f"  - Total de lecturas: {estadisticas['total_lecturas']}")
            print(f"  - Valor promedio: {estadisticas['valor_promedio']:.2f}" if estadisticas['valor_promedio'] else "  - Valor promedio: N/A")
            print(f"  - Valor mínimo: {estadisticas['valor_minimo']}" if estadisticas['valor_minimo'] else "  - Valor mínimo: N/A")
            print(f"  - Valor máximo: {estadisticas['valor_maximo']}" if estadisticas['valor_maximo'] else "  - Valor máximo: N/A")
        else:
            print(f"✗ Error al obtener estadísticas: {response.status_code}")
        
        # 8. Análisis de tendencia
        print("\n8. Analizando tendencia del sensor...")
        response = await client.get(f"{BASE_URL}/sensor/{id_sensor}/tendencia?limite_lecturas=10")
        if response.status_code == 200:
            tendencia = response.json()
            print(f"✓ Tendencia del sensor {id_sensor}:")
            print(f"  - Tendencia: {tendencia['tendencia']}")
            print(f"  - Porcentaje de cambio: {tendencia['porcentaje_cambio']}%")
            print(f"  - Valor inicial: {tendencia['valor_inicial']}")
            print(f"  - Valor final: {tendencia['valor_final']}")
        else:
            print(f"✗ Error al analizar tendencia: {response.status_code}")
        
        # 9. Obtener lecturas por rango de fechas
        print("\n9. Obteniendo lecturas por rango de fechas...")
        fecha_inicio = (datetime.now() - timedelta(hours=2)).isoformat()
        fecha_fin = datetime.now().isoformat()
        response = await client.get(f"{BASE_URL}/rango-fechas/?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}")
        if response.status_code == 200:
            lecturas_rango = response.json()
            print(f"✓ Lecturas en rango de fechas: {len(lecturas_rango)}")
        else:
            print(f"✗ Error al obtener lecturas por rango: {response.status_code}")
        
        # 10. Contar lecturas por sensor
        print("\n10. Contando lecturas por sensor...")
        response = await client.get(f"{BASE_URL}/sensor/{id_sensor}/contar")
        if response.status_code == 200:
            contador = response.json()
            print(f"✓ Total de lecturas del sensor {id_sensor}: {contador['total_lecturas']}")
        else:
            print(f"✗ Error al contar lecturas: {response.status_code}")
        
        # 11. Actualizar lectura
        print("\n11. Actualizando lectura...")
        lectura_id = lecturas_creadas[0]['id_lectura']
        datos_actualizacion = {
            "valor": 27.5,
            "unidad": "°C"
        }
        response = await client.put(f"{BASE_URL}/{lectura_id}", json=datos_actualizacion)
        if response.status_code == 200:
            lectura_actualizada = response.json()
            print(f"✓ Lectura actualizada: ID {lectura_actualizada['id_lectura']}, Nuevo valor: {lectura_actualizada['valor']}{lectura_actualizada['unidad']}")
        else:
            print(f"✗ Error al actualizar lectura: {response.status_code}")
        
        # 12. Eliminar lectura
        print("\n12. Eliminando lectura...")
        lectura_id = lecturas_creadas[-1]['id_lectura']
        response = await client.delete(f"{BASE_URL}/{lectura_id}")
        if response.status_code == 200:
            print(f"✓ Lectura eliminada: ID {lectura_id}")
        else:
            print(f"✗ Error al eliminar lectura: {response.status_code}")
        
        print("\n=== PRUEBAS COMPLETADAS ===")

async def test_validaciones():
    """Test de validaciones específicas"""
    
    async with httpx.AsyncClient() as client:
        print("\n=== PRUEBAS DE VALIDACIÓN ===\n")
        
        # Valor negativo
        print("1. Probando valor negativo...")
        response = await client.post(BASE_URL, json={
            "id_sensor": 1,
            "valor": -5.0,
            "unidad": "°C"
        })
        if response.status_code == 400:
            print("✓ Validación de valor negativo funcionando")
        else:
            print(f"✗ Error en validación de valor negativo: {response.status_code}")
        
        # Unidad inválida
        print("2. Probando unidad inválida...")
        response = await client.post(BASE_URL, json={
            "id_sensor": 1,
            "valor": 25.0,
            "unidad": "INVALID"
        })
        if response.status_code == 400:
            print("✓ Validación de unidad inválida funcionando")
        else:
            print(f"✗ Error en validación de unidad inválida: {response.status_code}")
        
        # ID sensor inválido
        print("3. Probando ID sensor inválido...")
        response = await client.post(BASE_URL, json={
            "id_sensor": 0,
            "valor": 25.0,
            "unidad": "°C"
        })
        if response.status_code == 400:
            print("✓ Validación de ID sensor inválido funcionando")
        else:
            print(f"✗ Error en validación de ID sensor inválido: {response.status_code}")
        
        print("\n=== PRUEBAS DE VALIDACIÓN COMPLETADAS ===")

def main():
    """Función principal para ejecutar las pruebas"""
    print("Iniciando pruebas del módulo de Lecturas...")
    print("Asegúrate de que la API esté corriendo en http://localhost:8000")
    input("Presiona Enter para continuar...")
    
    asyncio.run(test_lecturas_crud())
    asyncio.run(test_validaciones())

if __name__ == "__main__":
    main()
