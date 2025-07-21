"""
Diagnóstico detallado del API VOLTIO en producción
"""
import requests
import json

PROD_URL = 'https://voltioapi.acstree.xyz'
API_URL = f'{PROD_URL}/api/v1'

def detailed_diagnostics():
    """Realizar diagnóstico detallado"""
    print("🔍 DIAGNÓSTICO DETALLADO API VOLTIO")
    print("=" * 50)
    
    session = requests.Session()
    
    # 1. Verificar endpoints básicos sin autenticación
    basic_tests = [
        ("Root endpoint", "/"),
        ("OpenAPI schema", "/openapi.json"),
        ("Documentation", "/docs"),
    ]
    
    print("\n1️⃣ ENDPOINTS PÚBLICOS:")
    for name, endpoint in basic_tests:
        url = f"{PROD_URL}{endpoint}"
        try:
            response = session.get(url, timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {name}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: ERROR - {e}")
    
    # 2. Verificar endpoints de API que necesitan autenticación
    api_tests = [
        ("Users login", "POST", "/users/login", {"email": "test", "password": "test"}),
        ("Users list", "GET", "/users", None),
        ("Roles list", "GET", "/roles", None), 
        ("Health check", "GET", "/health", None),
    ]
    
    print("\n2️⃣ ENDPOINTS DE API:")
    for name, method, endpoint, data in api_tests:
        url = f"{API_URL}{endpoint}"
        try:
            if method == "GET":
                response = session.get(url, timeout=10)
            elif method == "POST":
                response = session.post(url, json=data, timeout=10)
            
            status_icon = "✅" if response.status_code < 400 else "⚠️" if response.status_code < 500 else "❌"
            print(f"   {status_icon} {name}: {response.status_code}")
            
            # Mostrar detalles del error si hay
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    detail = error_data.get('detail', 'No detail')
                    print(f"      📄 Detail: {detail}")
                except:
                    # Si no es JSON, mostrar texto plano
                    error_text = response.text[:100]
                    print(f"      📄 Error: {error_text}")
                    
        except Exception as e:
            print(f"   ❌ {name}: ERROR - {e}")
    
    # 3. Intentar diferentes credenciales de login
    print("\n3️⃣ PRUEBAS DE AUTENTICACIÓN:")
    login_tests = [
        ("Superadmin actual", {"email": "superadmin@voltio.com", "password": "SuperAdmin123!"}),
        ("Admin básico", {"email": "admin@example.com", "password": "admin123"}),
        ("Credenciales de prueba", {"email": "test@example.com", "password": "test123"}),
    ]
    
    for name, credentials in login_tests:
        try:
            response = session.post(f"{API_URL}/users/login", json=credentials, timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {name}: LOGIN EXITOSO")
                try:
                    data = response.json()
                    token = data.get('access_token', 'No token')[:20]
                    print(f"      🔑 Token: {token}...")
                except:
                    print(f"      📄 Response: {response.text[:50]}")
            else:
                print(f"   ❌ {name}: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"      📄 Error: {error_data.get('detail', 'No detail')}")
                except:
                    print(f"      📄 Response: {response.text[:50]}")
        except Exception as e:
            print(f"   ❌ {name}: ERROR - {e}")
    
    print("\n4️⃣ ANÁLISIS:")
    print("   🔍 Si los endpoints públicos funcionan pero los de API fallan,")
    print("      probablemente hay un problema con:")
    print("      - Configuración de base de datos")
    print("      - Variables de entorno")
    print("      - Túnel SSH si es necesario")
    print("      - Credenciales de la base de datos")
    
    session.close()

if __name__ == "__main__":
    detailed_diagnostics()
