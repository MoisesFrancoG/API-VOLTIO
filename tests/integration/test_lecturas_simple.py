"""
Script de prueba simple para verificar el módulo de Lecturas
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1/lecturas"

def test_basic_functionality():
    """Prueba básica del módulo de Lecturas"""
    
    print("🔍 Probando funcionalidad básica del módulo de Lecturas...")
    
    # 1. Crear una lectura de prueba
    print("\n1. Creando lectura de prueba...")
    lectura_data = {
        "id_sensor": 1,
        "valor": 25.5,
        "unidad": "°C",
        "fecha_hora": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(BASE_URL, json=lectura_data)
        if response.status_code == 200:
            lectura_creada = response.json()
            print(f"✅ Lectura creada: ID {lectura_creada['id_lectura']}")
            
            # 2. Obtener la lectura creada
            print("\n2. Obteniendo lectura creada...")
            lectura_id = lectura_creada['id_lectura']
            response = requests.get(f"{BASE_URL}/{lectura_id}")
            
            if response.status_code == 200:
                lectura_obtenida = response.json()
                print(f"✅ Lectura obtenida: {lectura_obtenida['valor']}{lectura_obtenida['unidad']}")
                
                # 3. Obtener todas las lecturas
                print("\n3. Obteniendo todas las lecturas...")
                response = requests.get(BASE_URL)
                
                if response.status_code == 200:
                    lecturas = response.json()
                    print(f"✅ Total de lecturas: {len(lecturas)}")
                    
                    # 4. Obtener lecturas por sensor
                    print("\n4. Obteniendo lecturas por sensor...")
                    response = requests.get(f"{BASE_URL}/sensor/1")
                    
                    if response.status_code == 200:
                        lecturas_sensor = response.json()
                        print(f"✅ Lecturas del sensor 1: {len(lecturas_sensor)}")
                        
                        print("\n🎉 TODAS LAS PRUEBAS BÁSICAS PASARON")
                        return True
                    else:
                        print(f"❌ Error al obtener lecturas por sensor: {response.status_code}")
                        print(f"   Detalle: {response.text}")
                else:
                    print(f"❌ Error al obtener todas las lecturas: {response.status_code}")
                    print(f"   Detalle: {response.text}")
            else:
                print(f"❌ Error al obtener lectura: {response.status_code}")
                print(f"   Detalle: {response.text}")
        else:
            print(f"❌ Error al crear lectura: {response.status_code}")
            print(f"   Detalle: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar a la API. Asegúrate de que esté ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
    
    return False

if __name__ == "__main__":
    print("🚀 Iniciando prueba simple del módulo de Lecturas")
    print("   Asegúrate de que la API esté corriendo en http://localhost:8000")
    
    input("\nPresiona Enter para continuar...")
    
    if test_basic_functionality():
        print("\n✅ El módulo de Lecturas está funcionando correctamente")
    else:
        print("\n❌ Hay problemas con el módulo de Lecturas")
