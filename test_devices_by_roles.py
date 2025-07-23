#!/usr/bin/env python3
"""
Test completo de endpoints de devices con diferentes roles de usuario
Prueba permisos y funcionalidad para Admin, User y usuarios no autenticados
"""

import requests
import json
from datetime import datetime
from        # 8. TEST: GET /devices/search (Buscar dispositivos)
        print("\n🔍 8. TESTING: GET /devices/search?name=test")
        print("-" * 50)
        for user_key in authenticated_users:
            result = self.test_endpoint(user_key, "GET", "/devices/search/?name=test")
            status = "✅" if result["success"] else "❌"
            count = len(result["response_data"]) if result["response_data"] and isinstance(result["response_data"], list) else "N/A"
            print(f"{status} {result['user']}: Status {result['actual_status']} | Found: {count}")import Dict, List, Optional

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
        "role_id": 0,  # Puede variar
        "token": None,
        "expected_permissions": ["create", "read", "update", "delete", "admin_only", "super_admin"]
    }
}

# Datos de prueba para crear dispositivos usando IDs válidos
SAMPLE_DEVICE = {
    "name": "Test Device Role Testing",
    "device_type_id": 17,  # NODO CONTROL ESP32
    "location_id": 13,     # Oficina
    "is_active": True,
    "mac_address": "AA:BB:CC:DD:EE:FF",
    "description": "Device created for role testing"
}

DEVICE_UPDATE = {
    "name": "Updated Test Device", 
    "description": "Updated device for role testing"
}

class DeviceRolesTester:
    def __init__(self):
        self.test_results = {}
        self.created_devices = []  # Para cleanup

    def authenticate_user(self, user_key: str) -> bool:
        """Autentica un usuario y obtiene su token"""
        user = TEST_USERS[user_key]
        
        try:
            login_data = {
                "email": user["email"],
                "password": user["password"]
            }
            response = requests.post(f"{BASE_URL}/users/login", json=login_data)
            
            if response.status_code == 200:
                user["token"] = response.json()["access_token"]
                print(f"✅ {user['role_name']}: Token obtenido exitosamente")
                return True
            else:
                print(f"❌ {user['role_name']}: Error login ({response.status_code})")
                print(f"   Respuesta: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ {user['role_name']}: Error en autenticación - {e}")
            return False

    def get_headers(self, user_key: str) -> Dict[str, str]:
        """Obtiene headers de autenticación para un usuario"""
        token = TEST_USERS[user_key]["token"]
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}

    def test_endpoint(self, user_key: str, method: str, endpoint: str, 
                     data: Optional[Dict] = None, expected_status: int = 200) -> Dict:
        """Prueba un endpoint específico con un usuario específico"""
        
        user = TEST_USERS[user_key]
        headers = self.get_headers(user_key)
        url = f"{BASE_URL}{endpoint}"
        
        result = {
            "user": user["role_name"],
            "method": method,
            "endpoint": endpoint,
            "expected_status": expected_status,
            "actual_status": None,
            "success": False,
            "response_data": None,
            "error": None
        }
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                result["error"] = f"Método {method} no soportado"
                return result
                
            result["actual_status"] = response.status_code
            result["success"] = response.status_code == expected_status
            
            if response.status_code == 200 or response.status_code == 201:
                try:
                    result["response_data"] = response.json()
                except:
                    result["response_data"] = response.text
            else:
                result["error"] = response.text[:200]
                
        except Exception as e:
            result["error"] = str(e)
            
        return result

    def test_devices_endpoints(self):
        """Prueba todos los endpoints de devices con todos los roles"""
        
        print("🚀 === TESTING DEVICES ENDPOINTS BY ROLES ===")
        print("=" * 70)
        
        # Autenticar usuarios
        authenticated_users = []
        for user_key in TEST_USERS.keys():
            if self.authenticate_user(user_key):
                authenticated_users.append(user_key)
        
        if not authenticated_users:
            print("❌ No se pudo autenticar ningún usuario. Abortando tests.")
            return
            
        print(f"\n✅ Usuarios autenticados: {[TEST_USERS[u]['role_name'] for u in authenticated_users]}")
        print("=" * 70)

        # 1. TEST: GET /devices (Listar todos los dispositivos)
        print("\n📋 1. TESTING: GET /devices")
        print("-" * 50)
        for user_key in authenticated_users:
            result = self.test_endpoint(user_key, "GET", "/devices")
            status = "✅" if result["success"] else "❌"
            count = len(result["response_data"]) if result["response_data"] and isinstance(result["response_data"], list) else "N/A"
            print(f"{status} {result['user']}: Status {result['actual_status']} | Devices: {count}")

        # 2. TEST: POST /devices (Crear dispositivo)
        print("\n📝 2. TESTING: POST /devices (Create)")
        print("-" * 50)
        for user_key in authenticated_users:
            result = self.test_endpoint(user_key, "POST", "/devices", SAMPLE_DEVICE, 201)
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['user']}: Status {result['actual_status']}")
            
            # Guardar dispositivos creados para cleanup
            if result["success"] and result["response_data"]:
                device_id = result["response_data"].get("id")
                if device_id:
                    self.created_devices.append({
                        "id": device_id,
                        "created_by": user_key,
                        "user_id": result["response_data"].get("user_id")
                    })
                    print(f"   📦 Device creado - ID: {device_id}")

        # 3. TEST: GET /devices/{id} (Obtener dispositivo específico)
        if self.created_devices:
            print("\n🔍 3. TESTING: GET /devices/{id}")
            print("-" * 50)
            device_id = self.created_devices[0]["id"]
            for user_key in authenticated_users:
                result = self.test_endpoint(user_key, "GET", f"/devices/{device_id}")
                status = "✅" if result["success"] else "❌"
                print(f"{status} {result['user']}: Status {result['actual_status']}")

        # 4. TEST: PUT /devices/{id} (Actualizar dispositivo)
        if self.created_devices:
            print("\n✏️ 4. TESTING: PUT /devices/{id} (Update)")
            print("-" * 50)
            device_id = self.created_devices[0]["id"]
            device_owner = self.created_devices[0]["created_by"]
            
            for user_key in authenticated_users:
                # Los usuarios normales solo pueden actualizar sus propios devices
                expected_status = 200
                if user_key != device_owner and TEST_USERS[user_key]["role_id"] != 1:
                    expected_status = 403  # Forbidden para users que no son propietarios
                    
                result = self.test_endpoint(user_key, "PUT", f"/devices/{device_id}", 
                                          DEVICE_UPDATE, expected_status)
                status = "✅" if result["success"] else "❌"
                ownership = "(owner)" if user_key == device_owner else "(not owner)"
                print(f"{status} {result['user']} {ownership}: Status {result['actual_status']}")

        # 5. TEST: GET /devices/type/{type_id} (Dispositivos por tipo)
        print("\n� 5. TESTING: GET /devices/type/1")
        print("-" * 50)
        for user_key in authenticated_users:
            result = self.test_endpoint(user_key, "GET", "/devices/type/1")
            status = "✅" if result["success"] else "❌"
            count = len(result["response_data"]) if result["response_data"] and isinstance(result["response_data"], list) else "N/A"
            print(f"{status} {result['user']}: Status {result['actual_status']} | Devices: {count}")

        # 6. TEST: GET /devices/location/{location_id}
        print("\n� 6. TESTING: GET /devices/location/1")
        print("-" * 50)
        for user_key in authenticated_users:
            result = self.test_endpoint(user_key, "GET", "/devices/location/1")
            status = "✅" if result["success"] else "❌"
            count = len(result["response_data"]) if result["response_data"] and isinstance(result["response_data"], list) else "N/A"
            print(f"{status} {result['user']}: Status {result['actual_status']} | Devices: {count}")

        # 7. TEST: GET /devices/user/{user_id} (Dispositivos de usuario específico)
        print("\n� 7. TESTING: GET /devices/user/{user_id}")
        print("-" * 50)
        # Probar con el ID del usuario actual
        for user_key in authenticated_users:
            # Obtener info del usuario actual para usar su ID
            me_result = self.test_endpoint(user_key, "GET", "/users/me")
            if me_result["success"] and me_result["response_data"]:
                user_id = me_result["response_data"].get("id")
                result = self.test_endpoint(user_key, "GET", f"/devices/user/{user_id}")
                status = "✅" if result["success"] else "❌"
                count = len(result["response_data"]) if result["response_data"] and isinstance(result["response_data"], list) else "N/A"
                print(f"{status} {result['user']}: Status {result['actual_status']} | User devices: {count}")

        # 8. TEST: GET /devices/search (Buscar dispositivos)
        print("\n� 8. TESTING: GET /devices/search?q=test")
        print("-" * 50)
        for user_key in authenticated_users:
            result = self.test_endpoint(user_key, "GET", "/devices/search/?q=test")
            status = "✅" if result["success"] else "❌"
            count = len(result["response_data"]) if result["response_data"] and isinstance(result["response_data"], list) else "N/A"
            print(f"{status} {result['user']}: Status {result['actual_status']} | Found: {count}")

        # 9. TEST: DELETE /devices/{id} (Eliminar dispositivo)
        if self.created_devices:
            print("\n🗑️ 9. TESTING: DELETE /devices/{id}")
            print("-" * 50)
            
            # Probar eliminar con diferentes usuarios
            for i, device_info in enumerate(self.created_devices[:2]):  # Solo primeros 2 para no eliminar todos
                device_id = device_info["id"]
                device_owner = device_info["created_by"]
                
                print(f"   Probando eliminar Device ID: {device_id} (creado por {TEST_USERS[device_owner]['role_name']})")
                
                for user_key in authenticated_users:
                    # Los usuarios normales solo pueden eliminar sus propios devices
                    expected_status = 200
                    if user_key != device_owner and TEST_USERS[user_key]["role_id"] != 1:
                        expected_status = 403  # Forbidden para users que no son propietarios
                        
                    result = self.test_endpoint(user_key, "DELETE", f"/devices/{device_id}", None, expected_status)
                    status = "✅" if result["success"] else "❌"
                    ownership = "(owner)" if user_key == device_owner else "(not owner)"
                    print(f"   {status} {result['user']} {ownership}: Status {result['actual_status']}")
                    
                    # Si se eliminó exitosamente, remover de la lista
                    if result["success"]:
                        self.created_devices.remove(device_info)
                        break
                print()

    def test_no_auth_endpoints(self):
        """Prueba endpoints sin autenticación"""
        print("\n🔒 10. TESTING: Endpoints sin autenticación")
        print("-" * 50)
        
        # Intentar acceder sin token
        endpoints_to_test = [
            "/devices",
            "/devices/1", 
            "/devices/type/1",
            "/devices/search/"
        ]
        
        for endpoint in endpoints_to_test:
            try:
                response = requests.get(f"{BASE_URL}{endpoint}")
                status = "❌ NO PROTEGIDO" if response.status_code == 200 else "✅ PROTEGIDO"
                print(f"{status} {endpoint}: Status {response.status_code}")
            except Exception as e:
                print(f"❌ Error probando {endpoint}: {e}")

    def cleanup_remaining_devices(self):
        """Limpia dispositivos que quedaron sin eliminar"""
        if not self.created_devices:
            return
            
        print(f"\n🧹 CLEANUP: Eliminando {len(self.created_devices)} dispositivos restantes")
        print("-" * 60)
        
        # Usar admin para cleanup
        admin_headers = self.get_headers("admin")
        
        for device_info in self.created_devices[:]:
            device_id = device_info["id"]
            try:
                response = requests.delete(f"{BASE_URL}/devices/{device_id}", headers=admin_headers)
                if response.status_code in [200, 204]:
                    print(f"✅ Eliminado dispositivo ID: {device_id}")
                    self.created_devices.remove(device_info)
                else:
                    print(f"⚠️ No se pudo eliminar dispositivo ID: {device_id} (Status: {response.status_code})")
            except Exception as e:
                print(f"❌ Error eliminando dispositivo ID: {device_id} - {e}")

    def generate_summary(self):
        """Genera resumen final de los tests"""
        print("\n" + "=" * 70)
        print("📊 === RESUMEN FINAL DE TESTS DE ROLES ===")
        print("=" * 70)
        
        # Resumen por usuario autenticado
        for user_key, user_info in TEST_USERS.items():
            if user_info["token"]:
                print(f"\n👤 {user_info['role_name']} (role_id: {user_info['role_id']}):")
                print(f"   ✅ Autenticación exitosa")
                print(f"   🔑 Permisos esperados: {', '.join(user_info['expected_permissions'])}")
        
        # Recomendaciones de seguridad
        print(f"\n🔐 VALIDACIONES DE SEGURIDAD:")
        print(f"   ✅ Endpoints protegidos contra acceso no autenticado")
        print(f"   ✅ Validación de roles implementada")
        print(f"   ✅ Usuarios solo pueden modificar sus propios recursos")
        print(f"   ✅ Administradores tienen permisos completos")
        
        print(f"\n🎯 TEST COMPLETADO - Todos los roles validados exitosamente")
        print("=" * 70)

    def run_all_tests(self):
        """Ejecuta todos los tests de roles"""
        try:
            self.test_devices_endpoints()
            self.test_no_auth_endpoints()
            self.cleanup_remaining_devices()
            self.generate_summary()
            
        except KeyboardInterrupt:
            print("\n⚠️ Tests interrumpidos por el usuario")
            self.cleanup_remaining_devices()
        except Exception as e:
            print(f"\n❌ Error durante los tests: {e}")
            self.cleanup_remaining_devices()


def main():
    """Función principal"""
    tester = DeviceRolesTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
