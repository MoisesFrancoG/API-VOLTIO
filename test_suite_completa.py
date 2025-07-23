#!/usr/bin/env python3
"""
🧪 API VOLTIO - Suite de Pruebas Automatizadas Completa
==========================================
Script de testing completo para todos los endpoints de la API VOLTIO
Versión: 2.0.0
Fecha: 22 de Julio 2025
==========================================
"""

import requests
import json
import time
import random
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass

# ==============================
# CONFIGURACIÓN
# ==============================

# URLs de la API
PROD_URL = "https://voltioapi.acstree.xyz"
DEV_URL = "http://127.0.0.1:8000"

# Seleccionar ambiente (cambiar según necesidad)
USE_PRODUCTION = True
BASE_URL = PROD_URL if USE_PRODUCTION else DEV_URL
API_URL = f"{BASE_URL}/api/v1"

# Credenciales de prueba
TEST_CREDENTIALS = {
    "superadmin": {
        "email": "superadmin@voltio.com",
        "password": "SuperAdmin123!"
    }
}

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==============================
# CLASES Y MODELOS
# ==============================

@dataclass
class EndpointTest:
    """Definición de una prueba de endpoint"""
    method: str
    endpoint: str
    description: str
    requires_auth: bool = True
    requires_admin: bool = False
    payload: Optional[dict] = None
    expected_status: int = 200
    category: str = "General"
    depends_on: Optional[List[str]] = None
    cleanup: bool = False

@dataclass
class TestResult:
    """Resultado de una prueba"""
    endpoint: str
    method: str
    status_code: int
    success: bool
    error: Optional[str] = None
    response_data: Optional[dict] = None
    execution_time: float = 0.0

class APITestSuite:
    """Suite completa de pruebas para la API VOLTIO"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 30
        self.tokens = {}
        self.test_data = {}  # Para almacenar IDs creados en tests
        self.results: List[TestResult] = []
        self.start_time = time.time()
        
        # Configurar headers por defecto
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'API-VOLTIO-AutoTest/2.0'
        })

    def log(self, message: str, level: str = "INFO"):
        """Logging personalizado con colores y formato"""
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "WARNING": "⚠️",
            "ERROR": "❌",
            "DEBUG": "🔍"
        }
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        icon = icons.get(level, "📝")
        print(f"[{timestamp}] {icon} {message}")
        
        if level in ["ERROR", "WARNING"]:
            logger.log(getattr(logging, level), message)

    def setup_authentication(self) -> bool:
        """Configurar autenticación para diferentes tipos de usuarios"""
        self.log("🔐 Configurando autenticación...")
        
        authenticated_users = 0
        
        for user_type, credentials in TEST_CREDENTIALS.items():
            try:
                response = self.session.post(
                    f"{API_URL}/users/login",
                    json=credentials,
                    timeout=10
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    self.tokens[user_type] = {
                        "token": token_data.get("access_token"),
                        "user": token_data.get("user"),
                        "headers": {"Authorization": f"Bearer {token_data.get('access_token')}"}
                    }
                    self.log(f"✅ Token obtenido para {user_type}: {credentials['email']}")
                    authenticated_users += 1
                else:
                    self.log(f"⚠️ Warning login {user_type}: {response.status_code}", "WARNING")
                    
            except Exception as e:
                self.log(f"⚠️ Warning autenticando {user_type}: {e}", "WARNING")
        
        # Solo requerimos al menos SuperAdmin
        if authenticated_users > 0 and "superadmin" in self.tokens:
            return True
        else:
            self.log("❌ Error crítico: No se pudo autenticar SuperAdmin", "ERROR")
            return False

    def make_request(self, method: str, endpoint: str, 
                     payload: Optional[dict] = None,
                     auth_type: str = "superadmin",
                     custom_headers: Optional[dict] = None) -> Tuple[int, dict, float]:
        """Realizar petición HTTP con manejo robusto de errores"""
        
        url = f"{API_URL}{endpoint}" if not endpoint.startswith('http') else endpoint
        
        # Preparar headers
        headers = {}
        if auth_type and auth_type in self.tokens:
            headers.update(self.tokens[auth_type]["headers"])
        if custom_headers:
            headers.update(custom_headers)

        start_time = time.time()
        
        try:
            # Hacer la petición según el método
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers)
            elif method.upper() == "POST":
                response = self.session.post(url, json=payload, headers=headers)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=payload, headers=headers)
            elif method.upper() == "PATCH":
                response = self.session.patch(url, json=payload, headers=headers)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")
                
            execution_time = time.time() - start_time
            
            # Intentar parsear JSON
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text[:500]}
                
            return response.status_code, response_data, execution_time
            
        except requests.exceptions.Timeout:
            return 408, {"error": "Request timeout"}, time.time() - start_time
        except requests.exceptions.ConnectionError:
            return 503, {"error": "Connection error"}, time.time() - start_time
        except Exception as e:
            return 500, {"error": str(e)}, time.time() - start_time

    def test_endpoint(self, test: EndpointTest) -> TestResult:
        """Ejecutar una prueba individual de endpoint"""
        
        # Determinar tipo de autenticación
        auth_type = None
        if test.requires_auth:
            auth_type = "superadmin" if test.requires_admin else "superadmin"
            
        # Realizar petición
        status_code, response_data, exec_time = self.make_request(
            test.method, test.endpoint, test.payload, auth_type
        )
        
        # Evaluar resultado
        success = status_code == test.expected_status
        error = None if success else f"Expected {test.expected_status}, got {status_code}"
        
        # Crear resultado
        result = TestResult(
            endpoint=test.endpoint,
            method=test.method,
            status_code=status_code,
            success=success,
            error=error,
            response_data=response_data,
            execution_time=exec_time
        )
        
        return result

    def generate_test_data(self):
        """Generar datos de prueba únicos"""
        timestamp = int(time.time())
        random_id = random.randint(1000, 9999)
        
        return {
            "user": {
                "username": f"TestUser{random_id}",  # CORREGIDO: era "name"
                "email": f"testuser{timestamp}@test.com",
                "password": "Test123!",
                "role_id": 2
            },
            "role": {
                "name": f"TestRole{random_id}",
                "description": f"Rol de prueba creado el {datetime.now().isoformat()}"
            },
            "location": {
                "name": f"TestLocation{random_id}",
                "description": f"Ubicación de prueba {timestamp}",
                "address": f"Test Address {random_id}"
            },
            "device_type": {
                "type_name": f"TestDeviceType{random_id}",  # CORREGIDO: era "name"
                "description": f"Tipo de dispositivo de prueba {timestamp}"
                # ELIMINADO: "category" que no existe en el schema
            },
            "device": {
                "name": f"TestDevice{random_id}",
                "mac_address": f"{random.randint(10,99):02X}:{random.randint(10,99):02X}:{random.randint(10,99):02X}:{random.randint(10,99):02X}:{random.randint(10,99):02X}:{random.randint(10,99):02X}",
                "description": f"Dispositivo de prueba {timestamp}",
                "is_active": True
            },
            "notification": {
                "title": f"Test Notification {random_id}",
                "message": f"Notificación de prueba creada el {datetime.now().isoformat()}",
                "notification_type": "info"
            },
            "device_command": {
                "command_name": f"TestCommand{random_id}",
                "command_type": "IR",
                "command_data": f"TEST_DATA_{timestamp}",
                "description": f"Comando de prueba {timestamp}"
            }
        }

    def define_test_endpoints(self) -> List[EndpointTest]:
        """Definir todos los endpoints a testear"""
        
        test_data = self.generate_test_data()
        
        tests = [
            # ===========================================
            # 🧪 ENDPOINTS DE PRUEBA Y MONITOREO
            # ===========================================
            EndpointTest("GET", "https://voltioapi.acstree.xyz/", "Root endpoint", False, False, None, 200, "System"),
            EndpointTest("GET", f"{BASE_URL}/test/quick", "Quick health check", False, False, None, 200, "System"),
            EndpointTest("GET", f"{BASE_URL}/test/health", "Health check", False, False, None, 200, "System"),
            EndpointTest("GET", f"{BASE_URL}/test/deployment", "Deployment info", False, False, None, 200, "System"),
            EndpointTest("GET", f"{BASE_URL}/test/system-info", "System info", False, False, None, 200, "System"),
            EndpointTest("GET", f"{BASE_URL}/test/database-check", "Database check", False, False, None, 200, "System"),
            EndpointTest("GET", f"{BASE_URL}/docs", "API Documentation", False, False, None, 200, "System"),
            
            # ===========================================
            # 👥 USUARIOS (USERS)
            # ===========================================
            # Endpoints públicos
            EndpointTest("POST", "/users/register", "Register new user", False, False, test_data["user"], 201, "Users"),
            EndpointTest("POST", "/users/login", "User login", False, False, TEST_CREDENTIALS["superadmin"], 200, "Users"),
            
            # Endpoints con autenticación
            EndpointTest("GET", "/users/me", "Current user info", True, False, None, 200, "Users"),
            EndpointTest("GET", "/users/", "List all users", True, False, None, 200, "Users"),
            EndpointTest("GET", "/users/1", "Get user by ID", True, False, None, 200, "Users"),
            EndpointTest("GET", f"/users/email/{TEST_CREDENTIALS['superadmin']['email']}", "Get user by email", True, False, None, 200, "Users"),
            
            # Endpoints admin
            EndpointTest("POST", "/users/", "Create user (admin)", True, True, test_data["user"], 201, "Users"),
            
            # ===========================================
            # 🏷️ ROLES
            # ===========================================
            EndpointTest("GET", "/roles/", "List roles", True, False, None, 200, "Roles"),
            EndpointTest("GET", "/roles/1", "Get role by ID", True, False, None, 200, "Roles"),
            EndpointTest("POST", "/roles/", "Create role", True, True, test_data["role"], 201, "Roles"),
            
            # ===========================================
            # 📍 UBICACIONES (LOCATIONS)
            # ===========================================
            EndpointTest("GET", "/locations/", "List locations", True, False, None, 200, "Locations"),
            EndpointTest("POST", "/locations/", "Create location", True, True, test_data["location"], 201, "Locations"),
            
            # ===========================================
            # 🔧 TIPOS DE DISPOSITIVOS (DEVICE TYPES)
            # ===========================================
            EndpointTest("GET", "/device-types/", "List device types", True, False, None, 200, "DeviceTypes"),
            EndpointTest("POST", "/device-types/", "Create device type", True, True, test_data["device_type"], 201, "DeviceTypes"),
            
            # ===========================================
            # 🔌 DISPOSITIVOS (DEVICES)
            # ===========================================
            EndpointTest("GET", "/devices/", "List devices", True, False, None, 200, "Devices"),
            EndpointTest("POST", "/devices/", "Create device", True, False, None, 201, "Devices"),  # Se configurará dinámicamente
            
            # ===========================================
            # 📡 COMANDOS IR
            # ===========================================
            EndpointTest("GET", "/device-commands/", "List device commands", True, False, None, 200, "DeviceCommands"),
            
            # ===========================================
            # 📊 LECTURAS PZEM
            # ===========================================
            EndpointTest("GET", "/lecturas-pzem/1h", "PZEM last hour readings", True, False, None, 200, "Readings"),
            EndpointTest("GET", "/lecturas-pzem/1d", "PZEM last day readings", True, False, None, 200, "Readings"),
            
            # ===========================================
            # 🔔 NOTIFICACIONES
            # ===========================================
            EndpointTest("GET", "/notifications/", "List notifications", True, False, None, 200, "Notifications"),
            EndpointTest("POST", "/notifications/", "Create notification", True, False, test_data["notification"], 201, "Notifications"),
        ]
        
        return tests

    def prepare_dynamic_tests(self, tests: List[EndpointTest]):
        """Preparar tests que requieren datos dinámicos"""
        
        # Obtener datos necesarios para crear dispositivo
        try:
            # Obtener ubicaciones
            status, locations_data, _ = self.make_request("GET", "/locations/")
            if status == 200 and locations_data and isinstance(locations_data, list) and len(locations_data) > 0:
                location_id = locations_data[0].get("id")
            else:
                location_id = 1  # fallback
                
            # Obtener tipos de dispositivos
            status, device_types_data, _ = self.make_request("GET", "/device-types/")
            if status == 200 and device_types_data and isinstance(device_types_data, list) and len(device_types_data) > 0:
                device_type_id = device_types_data[0].get("id")
            else:
                device_type_id = 1  # fallback
                
            # Configurar payload para crear dispositivo
            for test in tests:
                if test.endpoint == "/devices/" and test.method == "POST":
                    test.payload = {
                        "name": f"TestDevice{random.randint(1000, 9999)}",
                        "mac_address": f"{random.randint(10,99):02X}:{random.randint(10,99):02X}:{random.randint(10,99):02X}:{random.randint(10,99):02X}:{random.randint(10,99):02X}:{random.randint(10,99):02X}",
                        "device_type_id": device_type_id,
                        "location_id": location_id,
                        "description": "Dispositivo de prueba automatizada",
                        "is_active": True
                    }
                    
        except Exception as e:
            self.log(f"Error preparando tests dinámicos: {e}", "WARNING")

    def run_tests(self) -> Dict[str, any]:
        """Ejecutar toda la suite de pruebas"""
        
        self.log("🚀 INICIANDO SUITE DE PRUEBAS AUTOMATIZADAS API VOLTIO")
        self.log("=" * 70)
        self.log(f"🌐 Ambiente: {'PRODUCCIÓN' if USE_PRODUCTION else 'DESARROLLO'}")
        self.log(f"🔗 Base URL: {BASE_URL}")
        self.log(f"🕐 Tiempo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log("=" * 70)
        
        # Configurar autenticación
        if not self.setup_authentication():
            self.log("❌ Error crítico: No se pudo configurar autenticación", "ERROR")
            # Devolver reporte básico incluso si falla autenticación
            return {
                "timestamp": datetime.now().isoformat(),
                "environment": "production" if USE_PRODUCTION else "development",
                "base_url": BASE_URL,
                "total_tests": 0,
                "successful_tests": 0,
                "failed_tests": 0,
                "success_rate": 0,
                "execution_time": time.time() - self.start_time,
                "categories": {},
                "failed_tests_detail": [],
                "evaluation": "CRITICAL",
                "error": "Authentication failed"
            }
            
        # Definir y preparar tests
        tests = self.define_test_endpoints()
        self.prepare_dynamic_tests(tests)
        
        # Agrupar tests por categoría
        categories = {}
        for test in tests:
            if test.category not in categories:
                categories[test.category] = []
            categories[test.category].append(test)
        
        # Ejecutar tests por categoría
        for category, category_tests in categories.items():
            self.log(f"\n🧪 CATEGORÍA: {category.upper()}")
            self.log("-" * 50)
            
            for test in category_tests:
                self.log(f"🔄 {test.method} {test.endpoint} - {test.description}")
                
                result = self.test_endpoint(test)
                self.results.append(result)
                
                # Log del resultado
                if result.success:
                    self.log(f"   ✅ Status {result.status_code} ({result.execution_time:.3f}s)", "SUCCESS")
                else:
                    self.log(f"   ❌ Status {result.status_code} - {result.error} ({result.execution_time:.3f}s)", "ERROR")
                    
                # Guardar IDs importantes para tests posteriores
                if result.success and result.response_data and isinstance(result.response_data, dict):
                    if 'id' in result.response_data:
                        key = f"{category}_{test.method}_{test.endpoint.replace('/', '_')}"
                        self.test_data[key] = result.response_data.get('id')
                
                # Pequeña pausa entre requests
                time.sleep(0.1)
        
        return self.generate_report()

    def generate_report(self) -> Dict[str, any]:
        """Generar reporte completo de resultados"""
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        total_time = time.time() - self.start_time
        
        # Agrupar por categorías
        categories_stats = {}
        for result in self.results:
            # Inferir categoría del endpoint
            category = self._infer_category(result.endpoint)
            if category not in categories_stats:
                categories_stats[category] = {"total": 0, "success": 0, "failed": 0}
                
            categories_stats[category]["total"] += 1
            if result.success:
                categories_stats[category]["success"] += 1
            else:
                categories_stats[category]["failed"] += 1
        
        # Generar reporte
        self.log("\n" + "=" * 70)
        self.log("📊 REPORTE FINAL DE PRUEBAS AUTOMATIZADAS")
        self.log("=" * 70)
        
        self.log(f"📈 ESTADÍSTICAS GENERALES:")
        self.log(f"   • Total de pruebas: {total_tests}")
        self.log(f"   • Exitosas: {successful_tests} ✅")
        self.log(f"   • Fallidas: {failed_tests} ❌")
        self.log(f"   • Tasa de éxito: {success_rate:.1f}%")
        self.log(f"   • Tiempo total: {total_time:.2f}s")
        self.log(f"   • Ambiente: {'PRODUCCIÓN' if USE_PRODUCTION else 'DESARROLLO'}")
        
        self.log(f"\n📋 ESTADÍSTICAS POR CATEGORÍA:")
        for category, stats in categories_stats.items():
            rate = (stats["success"] / stats["total"] * 100) if stats["total"] > 0 else 0
            self.log(f"   • {category}: {stats['success']}/{stats['total']} ({rate:.1f}%)")
        
        # Mostrar errores si los hay
        failed_results = [r for r in self.results if not r.success]
        if failed_results:
            self.log(f"\n❌ PRUEBAS FALLIDAS ({len(failed_results)}):")
            for result in failed_results:
                self.log(f"   • {result.method} {result.endpoint}: {result.error}")
        
        # Evaluación final
        if success_rate >= 90:
            self.log("\n🎉 EVALUACIÓN: EXCELENTE - API funcionando perfectamente", "SUCCESS")
        elif success_rate >= 75:
            self.log("\n✅ EVALUACIÓN: BUENO - API funcionando correctamente", "SUCCESS")
        elif success_rate >= 50:
            self.log("\n⚠️ EVALUACIÓN: ACEPTABLE - Algunos problemas detectados", "WARNING")
        else:
            self.log("\n❌ EVALUACIÓN: CRÍTICO - Múltiples fallas detectadas", "ERROR")
        
        self.log("=" * 70)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "environment": "production" if USE_PRODUCTION else "development",
            "base_url": BASE_URL,
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "execution_time": total_time,
            "categories": categories_stats,
            "failed_tests_detail": [
                {
                    "endpoint": r.endpoint,
                    "method": r.method, 
                    "status_code": r.status_code,
                    "error": r.error
                } for r in failed_results
            ],
            "evaluation": self._get_evaluation(success_rate)
        }

    def _infer_category(self, endpoint: str) -> str:
        """Inferir categoría del endpoint"""
        if "/users" in endpoint:
            return "Users"
        elif "/roles" in endpoint:
            return "Roles"
        elif "/locations" in endpoint:
            return "Locations"
        elif "/device-types" in endpoint:
            return "DeviceTypes"
        elif "/devices" in endpoint:
            return "Devices"
        elif "/device-commands" in endpoint:
            return "DeviceCommands"
        elif "/lecturas-pzem" in endpoint:
            return "Readings"
        elif "/notifications" in endpoint:
            return "Notifications"
        elif "/test" in endpoint or endpoint == "/":
            return "System"
        else:
            return "Other"

    def _get_evaluation(self, success_rate: float) -> str:
        """Obtener evaluación basada en tasa de éxito"""
        if success_rate >= 90:
            return "EXCELLENT"
        elif success_rate >= 75:
            return "GOOD"
        elif success_rate >= 50:
            return "ACCEPTABLE"
        else:
            return "CRITICAL"

    def save_report_to_file(self, report: Dict[str, any], filename: str = None):
        """Guardar reporte en archivo JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            env = "prod" if USE_PRODUCTION else "dev"
            filename = f"api_test_report_{env}_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            self.log(f"📄 Reporte guardado en: {filename}")
        except Exception as e:
            self.log(f"Error guardando reporte: {e}", "ERROR")

def main():
    """Función principal"""
    
    print("🧪 API VOLTIO - Suite de Pruebas Automatizadas v2.0")
    print("===================================================")
    
    # Crear y ejecutar suite de pruebas
    suite = APITestSuite()
    
    try:
        report = suite.run_tests()
        
        # Guardar reporte
        suite.save_report_to_file(report)
        
        # Exit code basado en resultados
        if report["success_rate"] >= 75:
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Failure
            
    except KeyboardInterrupt:
        suite.log("\n🚫 Pruebas interrumpidas por el usuario", "WARNING")
        sys.exit(130)
    except Exception as e:
        suite.log(f"❌ Error fatal: {e}", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()
