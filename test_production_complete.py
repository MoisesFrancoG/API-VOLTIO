#!/usr/bin/env python3
"""
Script de pruebas completas para la API VOLTIO en producción
Versión: 2.0 - Sin túnel SSH
"""

import requests
import json
import time
from datetime import datetime
import sys

# Configuración
BASE_URL = "https://voltioapi.acstree.xyz"
API_BASE = f"{BASE_URL}/api/v1"

# Credenciales de prueba
TEST_USER = {
    "email": "superadmin@voltio.com", 
    "password": "SuperAdmin123!"
}

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.headers = {"Content-Type": "application/json"}
        
    def print_result(self, test_name, success, details=""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    └─ {details}")
        print()
    
    def test_health_check(self):
        """Verificar que la API esté respondiendo"""
        print("🔍 Verificando estado de la API...")
        try:
            # Probar el endpoint docs como health check
            response = self.session.get(f"{BASE_URL}/docs", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code} (usando /docs como health check)"
            if success:
                details += " | API respondiendo correctamente"
            self.print_result("Health Check", success, details)
            return success
        except Exception as e:
            self.print_result("Health Check", False, f"Error: {str(e)}")
            return False
    
    def test_docs(self):
        """Verificar documentación de la API"""
        print("📚 Verificando documentación...")
        try:
            response = self.session.get(f"{BASE_URL}/docs", timeout=10)
            success = response.status_code == 200 and "swagger" in response.text.lower()
            details = f"Status: {response.status_code}"
            self.print_result("API Documentation", success, details)
            return success
        except Exception as e:
            self.print_result("API Documentation", False, f"Error: {str(e)}")
            return False
    
    def test_login(self):
        """Probar autenticación"""
        print("🔐 Probando autenticación...")
        
        # Probar múltiples credenciales
        test_credentials = [
            {"email": "superadmin@voltio.com", "password": "SuperAdmin123!", "name": "SuperAdmin"},
            {"email": "admin@voltio.com", "password": "admin123", "name": "Admin"},
            {"email": "test@test.com", "password": "password", "name": "Test User"}
        ]
        
        for creds in test_credentials:
            try:
                print(f"   Probando {creds['name']}...")
                
                response = self.session.post(
                    f"{API_BASE}/users/login",
                    headers=self.headers,
                    json={"email": creds["email"], "password": creds["password"]},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "access_token" in data:
                        self.token = data["access_token"]
                        self.headers["Authorization"] = f"Bearer {self.token}"
                        details = f"Status: 200 | {creds['name']} login exitoso | Token obtenido"
                        self.print_result("Login Authentication", True, details)
                        return True
                    else:
                        print(f"   ❌ {creds['name']}: Token no encontrado en respuesta")
                else:
                    print(f"   ❌ {creds['name']}: Status {response.status_code}")
                    if response.status_code != 404:  # No mostrar detalles de 404
                        try:
                            error_data = response.json()
                            print(f"      Error: {error_data}")
                        except:
                            print(f"      Response: {response.text[:100]}")
                            
            except Exception as e:
                print(f"   ❌ {creds['name']}: Error {str(e)}")
        
        self.print_result("Login Authentication", False, "Ninguna credencial funcionó")
        return False
    
    def test_protected_endpoint(self, endpoint, name):
        """Probar un endpoint protegido"""
        if not self.token:
            self.print_result(f"Protected Endpoint - {name}", False, "No hay token de autenticación")
            return False
        
        try:
            response = self.session.get(
                f"{API_BASE}/{endpoint}",
                headers=self.headers,
                timeout=10
            )
            
            success = response.status_code in [200, 404]  # 404 es OK si no hay datos
            details = f"Status: {response.status_code}"
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        details += f" | Items: {len(data)}"
                    else:
                        details += f" | Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not dict'}"
                except:
                    details += " | Non-JSON response"
            elif response.status_code == 404:
                details += " | No data found (expected)"
            else:
                try:
                    error_data = response.json()
                    details += f" | Error: {error_data}"
                except:
                    details += f" | Response: {response.text[:200]}"
            
            self.print_result(f"Protected Endpoint - {name}", success, details)
            return success
        except Exception as e:
            self.print_result(f"Protected Endpoint - {name}", False, f"Error: {str(e)}")
            return False
    
    def test_database_endpoints(self):
        """Probar endpoints que requieren base de datos"""
        endpoints = [
            ("usuarios", "Usuarios"),
            ("roles", "Roles"),
            ("ubicaciones", "Ubicaciones"),
            ("tipo-sensores", "Tipo Sensores"),
            ("sensores", "Sensores"),
            ("lecturas", "Lecturas"),
            ("alertas", "Alertas"),
            ("comandos-ir", "Comandos IR")
        ]
        
        print("🗄️ Probando endpoints de base de datos...")
        results = []
        
        for endpoint, name in endpoints:
            result = self.test_protected_endpoint(endpoint, name)
            results.append(result)
            time.sleep(0.5)  # Pequeña pausa entre requests
        
        return results
    
    def test_create_data(self):
        """Probar creación de datos básicos"""
        if not self.token:
            self.print_result("Data Creation Tests", False, "No hay token de autenticación")
            return False
        
        print("📝 Probando creación de datos...")
        
        # Probar crear un rol
        try:
            rol_data = {
                "nombre": "Test Role",
                "descripcion": "Rol de prueba creado por script"
            }
            
            response = self.session.post(
                f"{API_BASE}/roles",
                headers=self.headers,
                json=rol_data,
                timeout=10
            )
            
            success = response.status_code in [200, 201, 409]  # 409 si ya existe
            details = f"Status: {response.status_code}"
            
            if response.status_code in [200, 201]:
                details += " | Rol creado exitosamente"
            elif response.status_code == 409:
                details += " | Rol ya existe (OK)"
            else:
                try:
                    error_data = response.json()
                    details += f" | Error: {error_data}"
                except:
                    details += f" | Response: {response.text[:200]}"
            
            self.print_result("Create Role Test", success, details)
            return success
        except Exception as e:
            self.print_result("Create Role Test", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print("=" * 60)
        print("🚀 INICIANDO PRUEBAS COMPLETAS DE LA API VOLTIO")
        print("=" * 60)
        print(f"URL Base: {BASE_URL}")
        print(f"Tiempo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()
        
        results = []
        
        # Pruebas básicas
        results.append(self.test_health_check())
        results.append(self.test_docs())
        
        # Autenticación
        auth_success = self.test_login()
        results.append(auth_success)
        
        if auth_success:
            # Pruebas de endpoints protegidos
            db_results = self.test_database_endpoints()
            results.extend(db_results)
            
            # Pruebas de creación
            results.append(self.test_create_data())
        else:
            print("⚠️ Saltando pruebas que requieren autenticación...")
        
        # Resumen final
        print("=" * 60)
        print("📊 RESUMEN DE PRUEBAS")
        print("=" * 60)
        
        passed = sum(results)
        total = len(results)
        percentage = (passed / total * 100) if total > 0 else 0
        
        print(f"✅ Pruebas exitosas: {passed}")
        print(f"❌ Pruebas fallidas: {total - passed}")
        print(f"📈 Porcentaje de éxito: {percentage:.1f}%")
        print()
        
        if percentage >= 80:
            print("🎉 ¡API funcionando correctamente!")
        elif percentage >= 60:
            print("⚠️ API parcialmente funcional - revisar errores")
        else:
            print("🚨 API con problemas serios - revisar configuración")
        
        print("=" * 60)
        
        return percentage >= 80

def main():
    """Función principal"""
    tester = APITester()
    success = tester.run_all_tests()
    
    # Código de salida
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
