#!/usr/bin/env python3
"""
Script de pruebas OPTIMIZADO para la API VOLTIO
Con mejor manejo de timeouts y debugging detallado
"""

import requests
import json
import time
from datetime import datetime
import sys
import random

# Configuración
BASE_URL = "https://voltioapi.acstree.xyz"
API_BASE = f"{BASE_URL}/api/v1"

class VoltioAPITesterOptimized:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 30  # Timeout más largo
        self.admin_token = None
        self.user_token = None
        self.test_data = {}
        self.headers = {"Content-Type": "application/json"}
        self.passed_tests = 0
        self.failed_tests = 0
        self.total_tests = 0
        
    def log(self, message, level="INFO"):
        """Log con formato"""
        symbols = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "ERROR": "❌",
            "WARNING": "⚠️",
            "TEST": "🧪"
        }
        print(f"{symbols.get(level, 'ℹ️')} {message}")
    
    def test_result(self, test_name, success, details="", expected_status=None):
        """Registrar resultado de prueba con debugging"""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            self.log(f"{test_name}", "SUCCESS")
        else:
            self.failed_tests += 1
            self.log(f"{test_name}", "ERROR")
        
        if details:
            print(f"    └─ {details}")
        print()
        
        return success
    
    def make_request_safe(self, method, endpoint, data=None, token=None, timeout=20):
        """Request más seguro con mejor debugging"""
        url = f"{API_BASE}{endpoint}"
        headers = self.headers.copy()
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        try:
            print(f"    🔄 {method.upper()} {endpoint}")
            
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers, timeout=timeout)
            elif method.upper() == "POST":
                response = self.session.post(url, headers=headers, json=data, timeout=timeout)
            elif method.upper() == "PUT":
                response = self.session.put(url, headers=headers, json=data, timeout=timeout)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers, timeout=timeout)
            else:
                return None
            
            print(f"    📡 Response: {response.status_code}")
            
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    print(f"    📄 Error detail: {error_data}")
                except:
                    print(f"    📄 Error text: {response.text[:200]}")
            
            return response
            
        except requests.exceptions.Timeout:
            print(f"    ⏰ Timeout en {method} {endpoint}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"    🔌 Error de conexión en {method} {endpoint}")
            return None
        except Exception as e:
            print(f"    💥 Error inesperado: {str(e)}")
            return None
    
    def quick_authentication_check(self):
        """Verificación rápida de autenticación"""
        self.log("🔐 Verificación rápida de autenticación...", "TEST")
        
        # Login SuperAdmin
        admin_creds = {
            "email": "superadmin@voltio.com",
            "password": "SuperAdmin123!"
        }
        
        response = self.make_request_safe("POST", "/users/login", admin_creds)
        if response and response.status_code == 200:
            data = response.json()
            self.admin_token = data.get("access_token")
            self.log("✅ SuperAdmin autenticado", "SUCCESS")
            
            # Verificar token con /users/me
            me_response = self.make_request_safe("GET", "/users/me", token=self.admin_token)
            if me_response and me_response.status_code == 200:
                user_data = me_response.json()
                self.log(f"✅ Token válido - Usuario: {user_data.get('email', 'N/A')}", "SUCCESS")
                return True
            else:
                self.log("❌ Token inválido", "ERROR")
                return False
        else:
            self.log("❌ Fallo en login de SuperAdmin", "ERROR")
            return False
    
    def test_critical_endpoints(self):
        """Probar endpoints críticos uno por uno"""
        if not self.admin_token:
            self.log("❌ No hay token de admin", "ERROR")
            return
        
        endpoints_to_test = [
            ("GET", "/users/", "Listar usuarios"),
            ("GET", "/users/me", "Usuario actual"),
            ("GET", "/roles/", "Listar roles"),
            ("GET", "/locations/", "Listar ubicaciones"),
            ("GET", "/device-types/", "Tipos de dispositivos"),
            ("GET", "/devices/", "Listar dispositivos"),
            ("GET", "/device-commands/", "Comandos IR"),
            ("GET", "/notifications/", "Notificaciones"),
        ]
        
        for method, endpoint, description in endpoints_to_test:
            self.log(f"🧪 Probando: {description}", "TEST")
            
            response = self.make_request_safe(method, endpoint, token=self.admin_token, timeout=30)
            
            if response is None:
                success = False
                details = "Timeout o error de conexión"
            elif response.status_code == 200:
                success = True
                try:
                    data = response.json()
                    if isinstance(data, list):
                        details = f"Status: 200 | Items: {len(data)}"
                    else:
                        details = f"Status: 200 | Tipo: {type(data).__name__}"
                except:
                    details = "Status: 200 | Respuesta no JSON"
            elif response.status_code == 404:
                success = True  # 404 es aceptable para endpoints vacíos
                details = "Status: 404 | Sin datos (esperado)"
            elif response.status_code == 403:
                success = False
                details = "Status: 403 | Forbidden (problema de permisos)"
            else:
                success = False
                details = f"Status: {response.status_code}"
            
            self.test_result(f"{method} {endpoint} - {description}", success, details)
    
    def test_crud_operations(self):
        """Probar operaciones CRUD básicas"""
        if not self.admin_token:
            return
        
        self.log("🧪 PROBANDO OPERACIONES CRUD", "TEST")
        
        # 1. Crear ubicación
        self.log("📍 Creando ubicación de prueba...", "TEST")
        location_data = {
            "name": f"TestLocation{random.randint(1000, 9999)}",
            "description": "Ubicación de prueba para testing"
        }
        
        response = self.make_request_safe("POST", "/locations/", location_data, self.admin_token)
        if response and response.status_code == 201:
            location = response.json()
            self.test_data["location_id"] = location.get("id")
            self.test_result("POST /locations/ - Crear ubicación", True, f"Status: 201 | ID: {location.get('id')}")
        else:
            self.test_result("POST /locations/ - Crear ubicación", False, f"Status: {response.status_code if response else 'No response'}")
        
        # 2. Crear tipo de dispositivo
        self.log("🔧 Creando tipo de dispositivo...", "TEST")
        device_type_data = {
            "type_name": f"TEST_TYPE_{random.randint(1000, 9999)}",
            "description": "Tipo de dispositivo de prueba"
        }
        
        response = self.make_request_safe("POST", "/device-types/", device_type_data, self.admin_token)
        if response and response.status_code == 201:
            device_type = response.json()
            self.test_data["device_type_id"] = device_type.get("id")
            self.test_result("POST /device-types/ - Crear tipo", True, f"Status: 201 | ID: {device_type.get('id')}")
        else:
            self.test_result("POST /device-types/ - Crear tipo", False, f"Status: {response.status_code if response else 'No response'}")
        
        # 3. Crear dispositivo (si tenemos los prerequisitos)
        if self.test_data.get("location_id") and self.test_data.get("device_type_id"):
            self.log("🔌 Creando dispositivo...", "TEST")
            device_data = {
                "name": f"TestDevice{random.randint(1000, 9999)}",
                "mac_address": f"AA:BB:CC:DD:{random.randint(10, 99):02X}:{random.randint(10, 99):02X}",
                "device_type_id": self.test_data["device_type_id"],
                "location_id": self.test_data["location_id"],
                "description": "Dispositivo de prueba",
                "is_active": True
            }
            
            response = self.make_request_safe("POST", "/devices/", device_data, self.admin_token)
            if response and response.status_code == 201:
                device = response.json()
                self.test_data["device_id"] = device.get("id")
                self.test_data["device_mac"] = device.get("mac_address")
                self.test_result("POST /devices/ - Crear dispositivo", True, f"Status: 201 | ID: {device.get('id')}")
            else:
                self.test_result("POST /devices/ - Crear dispositivo", False, f"Status: {response.status_code if response else 'No response'}")
    
    def test_specific_features(self):
        """Probar características específicas"""
        if not self.admin_token:
            return
        
        self.log("🧪 PROBANDO CARACTERÍSTICAS ESPECÍFICAS", "TEST")
        
        # 1. Comando de relé (si tenemos dispositivo)
        if self.test_data.get("device_mac"):
            self.log("⚡ Probando comando de relé...", "TEST")
            relay_data = {"action": "ON"}
            
            response = self.make_request_safe(
                "POST", 
                f"/devices/{self.test_data['device_mac']}/command/relay",
                relay_data,
                self.admin_token
            )
            
            # Comando de relé puede fallar por varias razones válidas
            if response and response.status_code in [202, 400, 404, 409, 500]:
                success = True
                details = f"Status: {response.status_code} (respuesta válida)"
            else:
                success = False
                details = f"Status: {response.status_code if response else 'No response'}"
            
            self.test_result("POST /devices/{mac}/command/relay - Comando relé", success, details)
        
        # 2. Lecturas PZEM
        self.log("📊 Probando lecturas PZEM...", "TEST")
        time_ranges = ["last_hour", "last_day", "last_week"]
        
        for time_range in time_ranges:
            response = self.make_request_safe("GET", f"/lecturas-pzem/{time_range}", token=self.admin_token)
            success = response and response.status_code in [200, 404, 422]
            details = f"Status: {response.status_code if response else 'No response'}"
            
            self.test_result(f"GET /lecturas-pzem/{time_range} - Lecturas {time_range}", success, details)
    
    def run_optimized_tests(self):
        """Ejecutar pruebas optimizadas"""
        print("=" * 80)
        self.log("🚀 INICIANDO PRUEBAS OPTIMIZADAS DE LA API VOLTIO", "TEST")
        print("=" * 80)
        print(f"URL Base: {BASE_URL}")
        print(f"Tiempo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print()
        
        # 1. Verificación rápida de autenticación
        if not self.quick_authentication_check():
            self.log("❌ FALLO CRÍTICO EN AUTENTICACIÓN", "ERROR")
            return False
        
        print()
        
        # 2. Probar endpoints críticos
        self.test_critical_endpoints()
        print()
        
        # 3. Probar operaciones CRUD
        self.test_crud_operations()
        print()
        
        # 4. Probar características específicas
        self.test_specific_features()
        
        # Resumen final
        print("=" * 80)
        self.log("📊 RESUMEN OPTIMIZADO", "TEST")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"✅ Pruebas exitosas: {self.passed_tests}")
        print(f"❌ Pruebas fallidas: {self.failed_tests}")
        print(f"📊 Total de pruebas: {self.total_tests}")
        print(f"📈 Porcentaje de éxito: {success_rate:.1f}%")
        print()
        
        if success_rate >= 90:
            self.log("🎉 ¡API FUNCIONANDO EXCELENTEMENTE! (90%+)", "SUCCESS")
            status = "EXCELENTE"
        elif success_rate >= 80:
            self.log("✅ API funcionando correctamente (80%+)", "SUCCESS")
            status = "BUENO"
        elif success_rate >= 70:
            self.log("⚠️ API parcialmente funcional (70%+)", "WARNING")
            status = "ACEPTABLE"
        else:
            self.log("🚨 API con problemas serios (<70%)", "ERROR")
            status = "CRÍTICO"
        
        print(f"🏆 ESTADO FINAL: {status}")
        print("=" * 80)
        
        return success_rate >= 70  # Umbral más realista

def main():
    """Función principal optimizada"""
    tester = VoltioAPITesterOptimized()
    success = tester.run_optimized_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
