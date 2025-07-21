#!/usr/bin/env python3
"""
Verificación específica del endpoint POST /devices/
"""

import requests
import json
import random

BASE_URL = "https://voltioapi.acstree.xyz"
API_BASE = f"{BASE_URL}/api/v1"

def test_post_devices():
    print("🔌 VERIFICACIÓN ESPECÍFICA DEL ENDPOINT POST /devices/")
    print("=" * 60)
    
    # 1. Autenticación
    print("🔐 Autenticando como SuperAdmin...")
    login_data = {
        "email": "superadmin@voltio.com",
        "password": "SuperAdmin123!"
    }
    
    session = requests.Session()
    response = session.post(f"{API_BASE}/users/login", json=login_data, timeout=10)
    
    if response.status_code != 200:
        print(f"❌ Error en login: {response.status_code}")
        return
    
    token = response.json().get("access_token")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    print("✅ Autenticación exitosa")
    
    # 2. Obtener datos necesarios
    print("\n📋 Obteniendo datos necesarios...")
    
    # Obtener ubicaciones
    locations_response = session.get(f"{API_BASE}/locations/", headers=headers)
    if locations_response.status_code == 200:
        locations = locations_response.json()
        if locations:
            location_id = locations[0].get("id")
            print(f"✅ Ubicación disponible: ID {location_id}")
        else:
            print("⚠️ No hay ubicaciones, creando una...")
            new_location = {
                "name": f"TestLocation{random.randint(1000, 9999)}",
                "description": "Ubicación para test de dispositivo"
            }
            loc_response = session.post(f"{API_BASE}/locations/", headers=headers, json=new_location)
            if loc_response.status_code == 201:
                location_id = loc_response.json().get("id")
                print(f"✅ Ubicación creada: ID {location_id}")
            else:
                print(f"❌ Error creando ubicación: {loc_response.status_code}")
                return
    else:
        print(f"❌ Error obteniendo ubicaciones: {locations_response.status_code}")
        return
    
    # Obtener tipos de dispositivos
    device_types_response = session.get(f"{API_BASE}/device-types/", headers=headers)
    if device_types_response.status_code == 200:
        device_types = device_types_response.json()
        if device_types:
            device_type_id = device_types[0].get("id")
            device_type_name = device_types[0].get("type_name", "N/A")
            print(f"✅ Tipo de dispositivo disponible: ID {device_type_id} ({device_type_name})")
        else:
            print("⚠️ No hay tipos de dispositivos disponibles")
            return
    else:
        print(f"❌ Error obteniendo tipos de dispositivos: {device_types_response.status_code}")
        return
    
    # 3. Crear dispositivo con datos completos
    print("\n🔌 Creando dispositivo...")
    
    mac_address = f"AA:BB:CC:DD:{random.randint(10, 99):02X}:{random.randint(10, 99):02X}"
    device_data = {
        "name": f"TestDevice{random.randint(1000, 9999)}",
        "mac_address": mac_address,
        "device_type_id": device_type_id,
        "location_id": location_id,
        "description": "Dispositivo de prueba específica",
        "is_active": True
    }
    
    print(f"📝 Datos del dispositivo:")
    print(f"   - Nombre: {device_data['name']}")
    print(f"   - MAC: {device_data['mac_address']}")
    print(f"   - Tipo ID: {device_data['device_type_id']}")
    print(f"   - Ubicación ID: {device_data['location_id']}")
    print(f"   - Activo: {device_data['is_active']}")
    
    # Hacer la petición POST
    print("\n📡 Enviando petición POST /devices/...")
    response = session.post(f"{API_BASE}/devices/", headers=headers, json=device_data, timeout=15)
    
    print(f"📊 Status Code: {response.status_code}")
    print(f"📄 Headers: {dict(response.headers)}")
    
    try:
        response_data = response.json()
        print(f"📋 Response JSON:")
        print(json.dumps(response_data, indent=2, ensure_ascii=False))
    except:
        print(f"📄 Response Text: {response.text}")
    
    # 4. Análisis del resultado
    print("\n🔍 ANÁLISIS DEL RESULTADO:")
    
    if response.status_code == 201:
        print("✅ CORRECTO: Status 201 - Dispositivo creado exitosamente")
    elif response.status_code == 200:
        print("⚠️ EXTRAÑO: Status 200 - Debería ser 201 para creación")
        try:
            data = response.json()
            if "id" in data:
                print("✅ Pero el dispositivo parece haberse creado (tiene ID)")
                device_id = data.get("id")
                
                # Verificar que realmente se creó
                print(f"\n🔍 Verificando si el dispositivo {device_id} existe...")
                check_response = session.get(f"{API_BASE}/devices/{device_id}", headers=headers)
                if check_response.status_code == 200:
                    print("✅ CONFIRMADO: El dispositivo se creó correctamente")
                    print("🐛 PROBLEMA: Solo el status code está mal (200 en lugar de 201)")
                else:
                    print("❌ PROBLEMA: El dispositivo no se creó realmente")
            else:
                print("❌ PROBLEMA: Response sin ID, creación fallida")
        except:
            print("❌ PROBLEMA: Response no válido")
    elif response.status_code == 409:
        print("⚠️ CONFLICTO: Dispositivo con esa MAC ya existe")
    elif response.status_code == 400:
        print("❌ DATOS INVÁLIDOS: Error en los datos enviados")
        try:
            error_data = response.json()
            print(f"📝 Detalles del error: {error_data}")
        except:
            pass
    elif response.status_code == 422:
        print("❌ ERROR DE VALIDACIÓN: Datos no cumplen validaciones")
        try:
            error_data = response.json()
            print(f"📝 Detalles de validación: {error_data}")
        except:
            pass
    else:
        print(f"❌ ERROR INESPERADO: Status {response.status_code}")
    
    # 5. Probar con datos diferentes
    print("\n🧪 PROBANDO CON DATOS ALTERNATIVOS...")
    
    # Intentar con datos mínimos
    minimal_device = {
        "name": f"MinimalDevice{random.randint(1000, 9999)}",
        "mac_address": f"BB:CC:DD:EE:{random.randint(10, 99):02X}:{random.randint(10, 99):02X}",
        "device_type_id": device_type_id,
        "location_id": location_id
    }
    
    print("📝 Probando con datos mínimos...")
    minimal_response = session.post(f"{API_BASE}/devices/", headers=headers, json=minimal_device, timeout=15)
    print(f"📊 Status (mínimos): {minimal_response.status_code}")
    
    if minimal_response.status_code in [200, 201]:
        print("✅ Datos mínimos funcionan")
    else:
        print("❌ Datos mínimos también fallan")
        try:
            error_data = minimal_response.json()
            print(f"📝 Error: {error_data}")
        except:
            print(f"📄 Response: {minimal_response.text[:200]}")

if __name__ == "__main__":
    test_post_devices()
