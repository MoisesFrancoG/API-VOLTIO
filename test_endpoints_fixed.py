#!/usr/bin/env python3
"""
Test completo de endpoints de devices con diferentes roles de usuario - CORREGIDO
Prueba permisos y funcionalidad para Admin, User y usuarios no autenticados
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

# Configuración
BASE_URL = "http://localhost:8000/api/v1"

# Usuarios de prueba con diferentes roles
TEST_USERS = {
    "admin": {
        "email": "admin@voltio.com",
        "password": "admin123",
        "role_name": "Admin",
        "role_id": 1,
        "token": None,
        "expected_permissions": ["create", "read", "update", "delete", "admin_only"]
    },
    "testuser": {
        "email": "roletest@voltio.com", 
        "password": "roletest123",
        "role_name": "Regular User",
        "role_id": 2,
        "token": None,
        "expected_permissions": ["create", "read", "update_own", "delete_own"]
    },
    "superadmin": {
        "email": "superadmin@voltio.com",
        "password": "SuperAdmin123!", 
        "role_name": "SuperAdmin",
        "role_id": 0,
        "token": None,
        "expected_permissions": ["create", "read", "update", "delete", "admin_only", "super_admin"]
    }
}

# Datos de prueba para crear dispositivos usando IDs válidos
SAMPLE_DEVICE = {
    "name": "Test Device Role Testing Fixed",
    "device_type_id": 17,  # NODO CONTROL ESP32
    "location_id": 13,     # Oficina
    "is_active": True,
    "mac_address": "BB:CC:DD:EE:FF:00",
    "description": "Device created for role testing - fixed version"
}

DEVICE_UPDATE = {
    "name": "Updated Test Device Fixed", 
    "description": "Updated device for role testing - fixed version"
}

def get_token(user_key: str):
    """Obtener token para un usuario específico"""
    user = TEST_USERS[user_key]
    login_data = {
        "email": user["email"],
        "password": user["password"]
    }
    
    response = requests.post(f"{BASE_URL}/users/login", json=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def test_corrected_endpoints():
    """Probar los endpoints corregidos específicamente"""
    
    print("🔧 === TESTING ENDPOINTS CORREGIDOS ===")
    print("="*50)
    
    # Obtener token de admin
    admin_token = get_token("admin")
    if not admin_token:
        print("❌ No se pudo obtener token admin")
        return
    
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # 1. TEST: POST /devices (debe funcionar ahora)
    print("\n📝 1. TESTING: POST /devices (corregido)")
    print("-"*40)
    
    response = requests.post(f"{BASE_URL}/devices/", json=SAMPLE_DEVICE, headers=admin_headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        device = response.json()
        device_id = device["id"]
        print(f"✅ Device creado exitosamente: ID {device_id}")
        
        # 2. TEST: PUT /devices/{id} (debe funcionar ahora)
        print(f"\n✏️ 2. TESTING: PUT /devices/{device_id} (corregido)")
        print("-"*40)
        
        update_response = requests.put(f"{BASE_URL}/devices/{device_id}", json=DEVICE_UPDATE, headers=admin_headers)
        print(f"Status: {update_response.status_code}")
        
        if update_response.status_code == 200:
            print("✅ Device actualizado exitosamente")
            print(f"Response: {update_response.json()}")
        else:
            print(f"❌ Error actualizando: {update_response.text}")
        
        # 3. TEST: GET /devices/user/{user_id} (debe funcionar ahora)
        print(f"\n👤 3. TESTING: GET /devices/user/1 (corregido)")
        print("-"*40)
        
        user_devices_response = requests.get(f"{BASE_URL}/devices/user/1", headers=admin_headers)
        print(f"Status: {user_devices_response.status_code}")
        
        if user_devices_response.status_code == 200:
            devices = user_devices_response.json()
            print(f"✅ Devices del usuario obtenidos: {len(devices)} devices")
        else:
            print(f"❌ Error obteniendo devices del usuario: {user_devices_response.text}")
        
        # 4. TEST: GET /devices/search?name=test (corregido)
        print(f"\n🔍 4. TESTING: GET /devices/search?name=Test (corregido)")
        print("-"*40)
        
        search_response = requests.get(f"{BASE_URL}/devices/search/?name=Test", headers=admin_headers)
        print(f"Status: {search_response.status_code}")
        
        if search_response.status_code == 200:
            found_devices = search_response.json()
            print(f"✅ Búsqueda exitosa: {len(found_devices)} devices encontrados")
        else:
            print(f"❌ Error en búsqueda: {search_response.text}")
        
        # 5. Cleanup: DELETE device
        print(f"\n🗑️ 5. CLEANUP: DELETE /devices/{device_id}")
        print("-"*40)
        
        delete_response = requests.delete(f"{BASE_URL}/devices/{device_id}", headers=admin_headers)
        print(f"Status: {delete_response.status_code}")
        
        if delete_response.status_code == 200:
            print("✅ Device eliminado exitosamente")
        else:
            print(f"❌ Error eliminando: {delete_response.text}")
            
    else:
        print(f"❌ Error creando device: {response.text}")
    
    # 6. TEST: Regular User POST /devices 
    print(f"\n👤 6. TESTING: Regular User POST /devices")  
    print("-"*40)
    
    regular_token = get_token("testuser")
    if regular_token:
        regular_headers = {"Authorization": f"Bearer {regular_token}"}
        
        regular_device = SAMPLE_DEVICE.copy()
        regular_device["name"] = "Regular User Test Device"
        regular_device["mac_address"] = "CC:DD:EE:FF:00:11"
        
        regular_response = requests.post(f"{BASE_URL}/devices/", json=regular_device, headers=regular_headers)
        print(f"Status: {regular_response.status_code}")
        
        if regular_response.status_code == 201:
            print("✅ Regular user puede crear devices")
            reg_device = regular_response.json()
            # Cleanup
            requests.delete(f"{BASE_URL}/devices/{reg_device['id']}", headers=regular_headers)
        else:
            print(f"❌ Regular user no puede crear devices: {regular_response.text}")
    else:
        print("❌ No se pudo autenticar regular user")

def main():
    test_corrected_endpoints()

if __name__ == "__main__":
    main()
