#!/usr/bin/env python3
"""
Test completo de endpoints de devices con manejo de errores de conexión
SuperAdmin vs Regular User
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

# Configuración
BASE_URL = "https://voltioapi.acstree.xyz/api/v1"

# Usuarios de prueba
TEST_USERS = {
    "superadmin": {
        "email": "superadmin@voltio.com",
        "password": "SuperAdmin123!",
        "role_name": "SuperAdmin",
        "role_id": 0,
        "token": None
    },
    "testuser": {
        "email": "roletest@voltio.com", 
        "password": "roletest123",
        "role_name": "Regular User",
        "role_id": 2,
        "token": None
    }
}

def make_request_with_retry(method, url, headers=None, json_data=None, max_retries=3):
    """Hace una petición HTTP con reintentos en caso de error de conexión"""
    for attempt in range(max_retries):
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=15)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=json_data, timeout=15)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=json_data, timeout=15)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=15)
            else:
                raise ValueError(f"Método {method} no soportado")
            
            return response
            
        except requests.exceptions.ConnectionError as e:
            print(f"   ⚠️ Intento {attempt + 1}/{max_retries} falló: {str(e)[:50]}...")
            if attempt < max_retries - 1:
                time.sleep(2)  # Esperar 2 segundos antes del siguiente intento
            else:
                raise e
        except Exception as e:
            raise e

def authenticate_user(user_key: str) -> bool:
    """Autentica un usuario con reintentos"""
    user = TEST_USERS[user_key]
    
    print(f"🔐 Autenticando {user['role_name']}...")
    
    login_data = {
        "email": user["email"],
        "password": user["password"]
    }
    
    try:
        response = make_request_with_retry("POST", f"{BASE_URL}/users/login", json_data=login_data)
        
        if response.status_code == 200:
            user["token"] = response.json()["access_token"]
            print(f"✅ {user['role_name']}: Autenticado exitosamente")
            return True
        else:
            print(f"❌ {user['role_name']}: Error ({response.status_code}) - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ {user['role_name']}: Error de conexión - {e}")
        return False

def get_headers(user_key: str) -> Dict[str, str]:
    """Obtiene headers de autenticación"""
    token = TEST_USERS[user_key]["token"]
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def test_endpoint(user_key: str, method: str, endpoint: str, data=None, expected_status=200):
    """Prueba un endpoint con reintentos"""
    user = TEST_USERS[user_key]
    headers = get_headers(user_key)
    url = f"{BASE_URL}{endpoint}"
    
    try:
        response = make_request_with_retry(method, url, headers=headers, json_data=data)
        
        success = response.status_code == expected_status
        response_data = None
        
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()
            except:
                response_data = response.text
        
        return {
            "success": success,
            "status": response.status_code,
            "data": response_data,
            "error": response.text if not success else None
        }
        
    except Exception as e:
        return {
            "success": False,
            "status": None,
            "data": None,
            "error": str(e)
        }

def run_comprehensive_test():
    """Ejecuta pruebas completas"""
    
    print("🚀 === TESTING DEVICES ENDPOINTS - SUPERADMIN vs REGULAR USER ===")
    print("=" * 80)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Autenticar usuarios
    authenticated_users = []
    for user_key in TEST_USERS.keys():
        if authenticate_user(user_key):
            authenticated_users.append(user_key)
    
    if len(authenticated_users) == 0:
        print("❌ No se pudo autenticar ningún usuario")
        return
    
    print(f"\n✅ Usuarios autenticados: {[TEST_USERS[u]['role_name'] for u in authenticated_users]}")
    print("=" * 80)
    
    created_devices = []
    
    # 1. GET /devices
    print("\n📋 1. TESTING: GET /devices")
    print("-" * 50)
    for user_key in authenticated_users:
        result = test_endpoint(user_key, "GET", "/devices")
        status = "✅" if result["success"] else "❌"
        count = len(result["data"]) if result["data"] and isinstance(result["data"], list) else "N/A"
        print(f"{status} {TEST_USERS[user_key]['role_name']}: Status {result['status']} | Devices: {count}")
    
    # 2. POST /devices
    print("\n📝 2. TESTING: POST /devices")
    print("-" * 50)
    for i, user_key in enumerate(authenticated_users):
        device_data = {
            "name": f"Test Device {TEST_USERS[user_key]['role_name']}",
            "device_type_id": 17,
            "location_id": 13,
            "is_active": True,
            "mac_address": f"FF:00:11:22:33:{44 + i:02X}",
            "description": f"Device created by {TEST_USERS[user_key]['role_name']}"
        }
        
        result = test_endpoint(user_key, "POST", "/devices", device_data, 201)
        status = "✅" if result["success"] else "❌"
        print(f"{status} {TEST_USERS[user_key]['role_name']}: Status {result['status']}")
        
        if result["success"] and result["data"]:
            device_id = result["data"].get("id")
            created_devices.append({
                "id": device_id,
                "created_by": user_key
            })
            print(f"   📦 Device creado - ID: {device_id}")
        elif not result["success"]:
            print(f"   📄 Error: {result['error'][:100] if result['error'] else 'Unknown error'}...")
    
    # 3. GET /devices/{id}
    if created_devices:
        print("\n🔍 3. TESTING: GET /devices/{id}")
        print("-" * 50)
        device_id = created_devices[0]["id"]
        for user_key in authenticated_users:
            result = test_endpoint(user_key, "GET", f"/devices/{device_id}")
            status = "✅" if result["success"] else "❌"
            print(f"{status} {TEST_USERS[user_key]['role_name']}: Status {result['status']}")
    
    # 4. PUT /devices/{id}
    if created_devices:
        print("\n✏️ 4. TESTING: PUT /devices/{id}")
        print("-" * 50)
        device_id = created_devices[0]["id"]
        device_owner = created_devices[0]["created_by"]
        
        update_data = {
            "name": "Updated Test Device",
            "description": "Updated by role test"
        }
        
        for user_key in authenticated_users:
            result = test_endpoint(user_key, "PUT", f"/devices/{device_id}", update_data)
            status = "✅" if result["success"] else "❌"
            ownership = "(owner)" if user_key == device_owner else "(not owner)"
            print(f"{status} {TEST_USERS[user_key]['role_name']} {ownership}: Status {result['status']}")
    
    # 5. GET /devices/search?name=Test
    print("\n🔍 5. TESTING: GET /devices/search?name=Test")
    print("-" * 50)
    for user_key in authenticated_users:
        result = test_endpoint(user_key, "GET", "/devices/search/?name=Test")
        status = "✅" if result["success"] else "❌"
        count = len(result["data"]) if result["data"] and isinstance(result["data"], list) else "N/A"
        print(f"{status} {TEST_USERS[user_key]['role_name']}: Status {result['status']} | Found: {count}")
    
    # 6. GET /devices/user/{user_id}
    print("\n👤 6. TESTING: GET /devices/user/{user_id}")
    print("-" * 50)
    for user_key in authenticated_users:
        # Obtener ID del usuario actual
        me_result = test_endpoint(user_key, "GET", "/users/me")
        if me_result["success"] and me_result["data"]:
            user_id = me_result["data"].get("id")
            result = test_endpoint(user_key, "GET", f"/devices/user/{user_id}")
            status = "✅" if result["success"] else "❌"
            count = len(result["data"]) if result["data"] and isinstance(result["data"], list) else "N/A"
            print(f"{status} {TEST_USERS[user_key]['role_name']}: Status {result['status']} | User devices: {count}")
    
    # 7. DELETE /devices/{id}
    if created_devices:
        print("\n🗑️ 7. TESTING: DELETE /devices/{id}")
        print("-" * 50)
        
        for device_info in created_devices:
            device_id = device_info["id"]
            device_owner = device_info["created_by"]
            
            print(f"   Eliminando Device ID: {device_id} (creado por {TEST_USERS[device_owner]['role_name']})")
            
            for user_key in authenticated_users:
                result = test_endpoint(user_key, "DELETE", f"/devices/{device_id}")
                status = "✅" if result["success"] else "❌"
                ownership = "(owner)" if user_key == device_owner else "(not owner)"
                print(f"   {status} {TEST_USERS[user_key]['role_name']} {ownership}: Status {result['status']}")
                
                if result["success"]:
                    break  # Si se eliminó, no intentar con otros usuarios
    
    # 8. Endpoints sin autenticación
    print("\n🔒 8. TESTING: Endpoints sin autenticación")
    print("-" * 50)
    
    endpoints = ["/devices", "/devices/1", "/devices/type/17", "/devices/search/"]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            status = "❌ NO PROTEGIDO" if response.status_code == 200 else "✅ PROTEGIDO"
            print(f"{status} {endpoint}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ Error probando {endpoint}: {e}")
    
    # Resumen final
    print("\n" + "=" * 80)
    print("📊 === RESUMEN FINAL ===")
    print("=" * 80)
    
    for user_key, user_info in TEST_USERS.items():
        if user_info["token"]:
            print(f"\n👤 {user_info['role_name']} (role_id: {user_info['role_id']}):")
            print(f"   ✅ Autenticación exitosa")
            print(f"   📧 Email: {user_info['email']}")
    
    print(f"\n🎯 PRUEBAS COMPLETADAS")
    print("=" * 80)

if __name__ == "__main__":
    run_comprehensive_test()
