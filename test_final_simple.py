#!/usr/bin/env python3
"""
🧪 PRUEBA FINAL SIMPLE - TODOS LOS ENDPOINTS API VOLTIO
Versión simplificada y robusta para verificación final
"""

import requests
import json
import time

BASE_URL = 'http://127.0.0.1:8000'
API_URL = f'{BASE_URL}/api/v1'
ADMIN_EMAIL = 'superadmin@voltio.com'
ADMIN_PASSWORD = 'SuperAdmin123!'


def test_simple():
    """Prueba simple de todos los endpoints principales"""
    print("🔥 PRUEBA FINAL - TODOS LOS ENDPOINTS")
    print("=" * 50)

    results = {'total': 0, 'passed': 0, 'failed': 0}

    def test(name, method, url, **kwargs):
        results['total'] += 1
        try:
            response = requests.request(method, url, timeout=5, **kwargs)
            if 200 <= response.status_code < 300:
                results['passed'] += 1
                print(f"✅ {name} - {response.status_code}")
                return response
            else:
                results['failed'] += 1
                print(f"❌ {name} - {response.status_code}")
                return response
        except Exception as e:
            results['failed'] += 1
            print(f"❌ {name} - Error: {str(e)[:50]}")
            return None

    # 1. CONECTIVIDAD BÁSICA
    print("\n📡 CONECTIVIDAD")
    test("Root", "GET", BASE_URL)
    test("Health", "GET", f"{BASE_URL}/test/health")
    test("Quick", "GET", f"{BASE_URL}/test/quick")

    # 2. AUTENTICACIÓN
    print("\n🔐 AUTENTICACIÓN")
    auth_response = test("Login", "POST", f"{API_URL}/users/login",
                         json={'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD})

    if not auth_response or auth_response.status_code != 200:
        print("❌ No se pudo autenticar. Abortando pruebas.")
        return

    token = auth_response.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    # 3. ENDPOINTS PRINCIPALES
    print("\n📋 ENDPOINTS PRINCIPALES")

    # Test endpoints
    test_endpoints = [
        "/test/deployment", "/test/deployment-v2", "/test/system-info",
        "/test/database-check", "/test/environment-vars", "/test/api-performance",
        "/test/all-endpoints"
    ]
    for endpoint in test_endpoints:
        test(f"Test {endpoint.split('/')[-1]}", "GET", f"{BASE_URL}{endpoint}")

    # Debug
    test("Debug Config", "GET", f"{BASE_URL}/debug/config")

    # API endpoints con autenticación
    api_endpoints = [
        ("Roles", "GET", "/roles"),
        ("Users", "GET", "/users"),
        ("Current User", "GET", "/users/me"),
        ("Locations", "GET", "/locations"),
        ("Device Types", "GET", "/device-types"),
        ("Devices", "GET", "/devices"),
        ("Device Commands", "GET", "/device-commands"),
        ("Notifications", "GET", "/notifications"),
    ]

    for name, method, endpoint in api_endpoints:
        test(name, method, f"{API_URL}{endpoint}", headers=headers)

    # 4. LECTURAS PZEM (probar diferentes rutas)
    print("\n📊 LECTURAS PZEM")
    pzem_paths = [
        "/api/v1/lecturas-pzem/1h",
        "/lecturas-pzem/1h",
        "/api/v1/readings/1h"
    ]

    for path in pzem_paths:
        response = test(f"PZEM {path}", "GET",
                        f"{BASE_URL}{path}", headers=headers)
        if response and response.status_code != 404:
            print(f"   ✅ Ruta correcta encontrada: {path}")
            break

    # 5. DOCUMENTACIÓN
    print("\n📚 DOCUMENTACIÓN")
    test("OpenAPI", "GET", f"{BASE_URL}/openapi.json")
    test("Swagger UI", "GET", f"{BASE_URL}/docs")
    test("ReDoc", "GET", f"{BASE_URL}/redoc")

    # 6. RESUMEN
    print("\n" + "=" * 50)
    print("📊 RESUMEN FINAL")
    print("=" * 50)

    total = results['total']
    passed = results['passed']
    failed = results['failed']
    success_rate = (passed / total * 100) if total > 0 else 0

    print(f"📈 Total de pruebas: {total}")
    print(f"✅ Exitosas: {passed}")
    print(f"❌ Fallidas: {failed}")
    print(f"📊 Tasa de éxito: {success_rate:.1f}%")

    if success_rate >= 90:
        print("\n🎉 EXCELENTE! La API está funcionando perfectamente")
        print("🚀 Lista para producción")
    elif success_rate >= 80:
        print("\n✅ MUY BUENO! La API funciona correctamente")
        print("💡 Algunos ajustes menores recomendados")
    elif success_rate >= 70:
        print("\n⚠️ BUENO! Funcionalidad principal operativa")
        print("🔧 Revisar endpoints fallidos")
    else:
        print("\n❌ CRÍTICO! Revisar problemas importantes")
        print("🚨 Requiere atención inmediata")

    print(f"\n🔗 API Docs: {BASE_URL}/docs")
    print(f"🔗 Health Check: {BASE_URL}/test/health")
    print("\n🏁 Prueba completada!")


if __name__ == "__main__":
    test_simple()
