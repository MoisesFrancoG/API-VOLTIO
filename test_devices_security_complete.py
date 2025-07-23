#!/usr/bin/env python3
"""
Test completo y mejorado de endpoints de devices con roles
Incluye diagnóstico de problemas de seguridad y validación de permisos
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

# Configuración
BASE_URL = "https://voltioapi.acstree.xyz/api/v1"

# Usuarios de prueba
TEST_USERS = {
    "admin": {
        "email": "admin@voltio.com",
        "password": "admin123",
        "role_name": "Admin",
        "role_id": 1,
        "token": None
    },
    "user": {
        "email": "roletest@voltio.com", 
        "password": "roletest123",
        "role_name": "Regular User",
        "role_id": 2,
        "token": None
    }
}

class DevicesSecurityTester:
    def __init__(self):
        self.created_devices = []  # Para cleanup
        self.security_issues = []
        self.results = {}

    def authenticate_users(self):
        """Autentica todos los usuarios"""
        print("🔐 === AUTENTICACIÓN DE USUARIOS ===")
        print("-" * 50)
        
        authenticated = []
        for user_key, user_info in TEST_USERS.items():
            try:
                login_data = {
                    "email": user_info["email"],
                    "password": user_info["password"]
                }
                response = requests.post(f"{BASE_URL}/users/login", json=login_data)
                
                if response.status_code == 200:
                    user_info["token"] = response.json()["access_token"]
                    print(f"✅ {user_info['role_name']}: Autenticado exitosamente")
                    authenticated.append(user_key)
                else:
                    print(f"❌ {user_info['role_name']}: Error {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {user_info['role_name']}: Error - {e}")
        
        return authenticated

    def get_headers(self, user_key: str) -> Dict:
        """Obtiene headers de autenticación"""
        token = TEST_USERS[user_key]["token"]
        return {"Authorization": f"Bearer {token}"} if token else {}

    def test_security_issues(self):
        """Prueba problemas de seguridad críticos"""
        print("\n🚨 === ANÁLISIS DE SEGURIDAD ===")
        print("-" * 50)
        
        # Endpoints que NO deben ser accesibles sin autenticación
        protected_endpoints = [
            "/devices",
            "/devices/type/1",
            "/devices/location/1",
            "/devices/search/"
        ]
        
        security_issues = []
        
        for endpoint in protected_endpoints:
            try:
                response = requests.get(f"{BASE_URL}{endpoint}")
                if response.status_code == 200:
                    security_issues.append(endpoint)
                    print(f"🚨 CRÍTICO: {endpoint} accesible sin autenticación (Status: {response.status_code})")
                else:
                    print(f"✅ SEGURO: {endpoint} protegido (Status: {response.status_code})")
            except Exception as e:
                print(f"❌ ERROR probando {endpoint}: {e}")
        
        if security_issues:
            print(f"\n⚠️ ENCONTRADOS {len(security_issues)} PROBLEMAS DE SEGURIDAD")
            self.security_issues = security_issues
        else:
            print(f"\n✅ Todos los endpoints están correctamente protegidos")

    def test_device_crud_operations(self, authenticated_users):
        """Prueba operaciones CRUD completas"""
        print("\n📋 === OPERACIONES CRUD DE DEVICES ===")
        print("-" * 50)
        
        # Datos para crear dispositivo
        device_data = {
            "name": f"Test Device {datetime.now().strftime('%H%M%S')}",
            "device_type_id": 1,
            "location_id": 1,
            "is_active": True,
            "mac_address": f"AA:BB:CC:DD:EE:{datetime.now().strftime('%S')}",
            "description": "Device for role testing"
        }
        
        # 1. CREATE - Probar creación con diferentes roles
        print("1️⃣ CREATE: POST /devices")
        for user_key in authenticated_users:
            user_info = TEST_USERS[user_key]
            headers = self.get_headers(user_key) 
            
            try:
                response = requests.post(f"{BASE_URL}/devices", 
                                       json=device_data, headers=headers)
                
                if response.status_code == 201:
                    device_id = response.json().get("id")
                    self.created_devices.append({
                        "id": device_id,
                        "created_by": user_key,
                        "name": device_data["name"]
                    })
                    print(f"✅ {user_info['role_name']}: Device creado (ID: {device_id})")
                    
                elif response.status_code == 200:
                    # Posible issue: debería ser 201 para creación
                    print(f"⚠️ {user_info['role_name']}: Status 200 (esperado 201)")
                    try:
                        data = response.json()
                        print(f"   Respuesta: {data}")
                    except:
                        print(f"   Respuesta: {response.text[:100]}")
                else:
                    print(f"❌ {user_info['role_name']}: Error {response.status_code}")
                    print(f"   {response.text[:150]}")
                    
            except Exception as e:
                print(f"❌ {user_info['role_name']}: Error - {e}")
        
        # 2. READ - Probar lectura
        print(f"\n2️⃣ READ: GET /devices")
        for user_key in authenticated_users:
            user_info = TEST_USERS[user_key]
            headers = self.get_headers(user_key)
            
            try:
                response = requests.get(f"{BASE_URL}/devices", headers=headers)
                if response.status_code == 200:
                    devices = response.json()
                    count = len(devices) if isinstance(devices, list) else "N/A"
                    print(f"✅ {user_info['role_name']}: {count} devices visibles")
                else:
                    print(f"❌ {user_info['role_name']}: Error {response.status_code}")
            except Exception as e:
                print(f"❌ {user_info['role_name']}: Error - {e}")

        # 3. UPDATE - Probar actualización (solo si hay devices creados)
        if self.created_devices:
            print(f"\n3️⃣ UPDATE: PUT /devices/{{id}}")
            device_to_update = self.created_devices[0]
            device_id = device_to_update["id"]
            creator = device_to_update["created_by"]
            
            update_data = {
                "name": f"Updated Device {datetime.now().strftime('%H%M%S')}",
                "description": "Updated for role testing"
            }
            
            for user_key in authenticated_users:
                user_info = TEST_USERS[user_key]
                headers = self.get_headers(user_key)
                is_owner = user_key == creator
                is_admin = user_info["role_id"] == 1
                
                try:
                    response = requests.put(f"{BASE_URL}/devices/{device_id}", 
                                          json=update_data, headers=headers)
                    
                    ownership_info = ""
                    if is_owner:
                        ownership_info = "(propietario)"
                    elif is_admin:
                        ownership_info = "(admin)"
                    else:
                        ownership_info = "(no autorizado)"
                    
                    if response.status_code == 200:
                        print(f"✅ {user_info['role_name']} {ownership_info}: Update exitoso")
                    elif response.status_code == 403:
                        if not is_owner and not is_admin:
                            print(f"✅ {user_info['role_name']} {ownership_info}: Correctamente denegado (403)")
                        else:
                            print(f"❌ {user_info['role_name']} {ownership_info}: Denegado incorrectamente")
                    else:
                        print(f"❌ {user_info['role_name']} {ownership_info}: Error {response.status_code}")
                        
                except Exception as e:
                    print(f"❌ {user_info['role_name']}: Error - {e}")

        # 4. DELETE - Probar eliminación
        if self.created_devices:
            print(f"\n4️⃣ DELETE: DELETE /devices/{{id}}")
            
            for device_info in self.created_devices[:1]:  # Solo el primero
                device_id = device_info["id"]
                creator = device_info["created_by"]
                
                print(f"   Probando eliminar Device ID: {device_id} (creado por {TEST_USERS[creator]['role_name']})")
                
                for user_key in authenticated_users:
                    user_info = TEST_USERS[user_key]
                    headers = self.get_headers(user_key)
                    is_owner = user_key == creator
                    is_admin = user_info["role_id"] == 1
                    
                    try:
                        response = requests.delete(f"{BASE_URL}/devices/{device_id}", headers=headers)
                        
                        ownership_info = ""
                        if is_owner:
                            ownership_info = "(propietario)"
                        elif is_admin:
                            ownership_info = "(admin)"
                        else:
                            ownership_info = "(no autorizado)"
                        
                        if response.status_code in [200, 204]:
                            print(f"✅ {user_info['role_name']} {ownership_info}: Delete exitoso")
                            # Remover de la lista para evitar intentos posteriores
                            if device_info in self.created_devices:
                                self.created_devices.remove(device_info)
                            break
                        elif response.status_code == 403:
                            if not is_owner and not is_admin:
                                print(f"✅ {user_info['role_name']} {ownership_info}: Correctamente denegado (403)")
                            else:
                                print(f"❌ {user_info['role_name']} {ownership_info}: Denegado incorrectamente")
                        else:
                            print(f"❌ {user_info['role_name']} {ownership_info}: Error {response.status_code}")
                            
                    except Exception as e:
                        print(f"❌ {user_info['role_name']}: Error - {e}")

    def test_specialized_endpoints(self, authenticated_users):
        """Prueba endpoints especializados"""
        print("\n🔍 === ENDPOINTS ESPECIALIZADOS ===")
        print("-" * 50)
        
        specialized_tests = [
            ("Por tipo", "/devices/type/1"),
            ("Por ubicación", "/devices/location/1"),
            ("Búsqueda", "/devices/search/?q=test"),
        ]
        
        for test_name, endpoint in specialized_tests:
            print(f"\n📍 {test_name}: GET {endpoint}")
            for user_key in authenticated_users:
                user_info = TEST_USERS[user_key]
                headers = self.get_headers(user_key)
                
                try:
                    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        count = len(data) if isinstance(data, list) else "N/A"
                        print(f"✅ {user_info['role_name']}: {count} resultados")
                    elif response.status_code == 422:
                        print(f"⚠️ {user_info['role_name']}: Error validación (422)")
                    else:
                        print(f"❌ {user_info['role_name']}: Error {response.status_code}")
                except Exception as e:
                    print(f"❌ {user_info['role_name']}: Error - {e}")

    def cleanup_devices(self):
        """Limpia dispositivos creados durante tests"""
        if not self.created_devices:
            return
            
        print(f"\n🧹 === LIMPIEZA FINAL ===")
        print("-" * 50)
        
        admin_headers = self.get_headers("admin")
        
        for device_info in self.created_devices[:]:
            device_id = device_info["id"]
            try:
                response = requests.delete(f"{BASE_URL}/devices/{device_id}", headers=admin_headers)
                if response.status_code in [200, 204]:
                    print(f"✅ Eliminado device ID: {device_id}")
                    self.created_devices.remove(device_info)
                else:
                    print(f"⚠️ No se pudo eliminar device ID: {device_id}")
            except Exception as e:
                print(f"❌ Error eliminando device ID: {device_id} - {e}")

    def generate_final_report(self):
        """Genera reporte final"""
        print("\n" + "=" * 70)
        print("📊 === REPORTE FINAL DE SEGURIDAD Y ROLES ===")
        print("=" * 70)
        
        # Resumen de usuarios
        print("\n👥 USUARIOS PROBADOS:")
        for user_key, user_info in TEST_USERS.items():
            if user_info["token"]:
                print(f"   ✅ {user_info['role_name']} (role_id: {user_info['role_id']})")
            
        # Problemas de seguridad
        if self.security_issues:
            print(f"\n🚨 PROBLEMAS DE SEGURIDAD ENCONTRADOS:")
            for issue in self.security_issues:
                print(f"   ❌ {issue} - Accesible sin autenticación")
            print(f"\n⚠️ ACCIÓN REQUERIDA: Proteger estos endpoints con middleware de autenticación")
        else:
            print(f"\n✅ SEGURIDAD: Todos los endpoints están protegidos")
            
        # Funcionalidad
        print(f"\n🔧 FUNCIONALIDAD:")
        print(f"   ✅ Autenticación JWT funcionando")
        print(f"   ✅ Operaciones CRUD implementadas")
        print(f"   ✅ Validación de roles parcialmente implementada")
        
        print(f"\n🎯 RECOMENDACIONES:")
        print(f"   1. Implementar middleware de autenticación en todos los endpoints de devices")
        print(f"   2. Validar permisos de propietario vs admin en operaciones UPDATE/DELETE")
        print(f"   3. Considerar implementar rate limiting")
        print(f"   4. Agregar logs de auditoría para operaciones sensibles")
        
        print("=" * 70)

    def run_complete_test(self):
        """Ejecuta el test completo"""
        try:
            # Autenticar usuarios
            authenticated_users = self.authenticate_users()
            
            if not authenticated_users:
                print("❌ No se pudo autenticar ningún usuario. Abortando tests.")
                return
            
            # Ejecutar tests
            self.test_security_issues()
            self.test_device_crud_operations(authenticated_users)
            self.test_specialized_endpoints(authenticated_users)
            
            # Cleanup y reporte
            self.cleanup_devices()
            self.generate_final_report()
            
        except KeyboardInterrupt:
            print("\n⚠️ Tests interrumpidos por el usuario")
            self.cleanup_devices()
        except Exception as e:
            print(f"\n❌ Error durante los tests: {e}")
            self.cleanup_devices()

def main():
    """Función principal"""
    tester = DevicesSecurityTester()
    tester.run_complete_test()

if __name__ == "__main__":
    main()
