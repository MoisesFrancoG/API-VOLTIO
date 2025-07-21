"""
Pruebas del API VOLTIO en producción - https://voltioapi.acstree.xyz
"""
import requests
import json
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# URL del servidor de producción
PROD_URL = 'https://voltioapi.acstree.xyz'
API_URL = f'{PROD_URL}/api/v1'


def create_robust_session():
    """Crear sesión con reintentos automáticos"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def test_basic_endpoints():
    """Probar endpoints básicos del API"""
    print("🚀 Probando API VOLTIO en PRODUCCIÓN")
    print("=" * 60)
    print(f"🌐 URL: {PROD_URL}")
    print(f"📍 API: {API_URL}")
    
    session = create_robust_session()
    
    tests = [
        ("🏠 Homepage", "GET", PROD_URL),
        ("📚 Documentation", "GET", f"{PROD_URL}/docs"),
        ("📋 OpenAPI JSON", "GET", f"{PROD_URL}/openapi.json"),
        ("🏥 Health Check", "GET", f"{API_URL}/health"),
        ("👥 Users endpoint", "GET", f"{API_URL}/users"),
        ("🏢 Roles endpoint", "GET", f"{API_URL}/roles"),
        ("📍 Locations endpoint", "GET", f"{API_URL}/locations"), 
        ("🔧 Device Types endpoint", "GET", f"{API_URL}/device-types"),
        ("📱 Devices endpoint", "GET", f"{API_URL}/devices"),
    ]
    
    results = []
    
    for test_name, method, url in tests:
        print(f"\n{test_name}")
        print(f"   {method} {url}")
        
        try:
            response = session.request(method, url, timeout=10)
            status = "✅" if response.status_code < 400 else "⚠️" if response.status_code < 500 else "❌"
            print(f"   {status} Status: {response.status_code}")
            
            # Intentar mostrar contenido relevante
            if response.status_code == 200:
                try:
                    if 'application/json' in response.headers.get('content-type', ''):
                        data = response.json()
                        if isinstance(data, list):
                            print(f"   📊 Items: {len(data)}")
                        elif isinstance(data, dict):
                            if 'message' in data:
                                print(f"   💬 Message: {data['message']}")
                            else:
                                print(f"   📊 Keys: {list(data.keys())[:5]}")
                    else:
                        content_length = len(response.text)
                        print(f"   📄 Content length: {content_length} chars")
                except:
                    print(f"   📄 Content type: {response.headers.get('content-type', 'unknown')}")
            
            results.append({
                'test': test_name,
                'method': method,
                'url': url,
                'status': response.status_code,
                'success': response.status_code < 400
            })
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error: {e}")
            results.append({
                'test': test_name,
                'method': method, 
                'url': url,
                'status': 'ERROR',
                'success': False
            })
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            results.append({
                'test': test_name,
                'method': method,
                'url': url, 
                'status': 'ERROR',
                'success': False
            })
    
    # Resumen
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"\n📊 RESUMEN DE PRUEBAS:")
    print(f"   ✅ Exitosas: {successful}/{total} ({successful/total*100:.1f}%)")
    print(f"   ❌ Fallidas: {total-successful}/{total}")
    
    if successful == total:
        print("\n🎉 ¡TODAS las pruebas básicas PASARON!")
    elif successful > total/2:
        print(f"\n✅ Mayoría de pruebas exitosas ({successful/total*100:.1f}%)")
    else:
        print(f"\n⚠️ Muchas pruebas fallaron ({successful/total*100:.1f}% exitosas)")
    
    session.close()
    return results


def test_authentication():
    """Probar autenticación con superadmin"""
    print(f"\n🔐 PROBANDO AUTENTICACIÓN")
    print("=" * 40)
    
    session = create_robust_session()
    
    # Intentar login con superadmin
    login_data = {
        'email': 'superadmin@voltio.com',
        'password': 'SuperAdmin123!'
    }
    
    try:
        print("🔑 Intentando login con superadmin...")
        response = session.post(f'{API_URL}/users/login', json=login_data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            if token:
                print("✅ Autenticación EXITOSA")
                print(f"   🔑 Token recibido: {token[:20]}...")
                
                # Probar un endpoint autenticado
                headers = {'Authorization': f'Bearer {token}'}
                auth_response = session.get(f'{API_URL}/users/me', headers=headers, timeout=10)
                
                if auth_response.status_code == 200:
                    user_data = auth_response.json()
                    print(f"✅ Endpoint autenticado funciona")
                    print(f"   👤 Usuario: {user_data.get('email', 'N/A')}")
                    print(f"   🏷️ Rol: {user_data.get('role_name', 'N/A')}")
                    return token
                else:
                    print(f"⚠️ Token válido pero endpoint /users/me falló: {auth_response.status_code}")
                    return token
            else:
                print("❌ Login exitoso pero sin token en respuesta")
                return None
        else:
            print(f"❌ Login falló: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   📄 Error: {error_data}")
            except:
                print(f"   📄 Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Error en autenticación: {e}")
        return None
    finally:
        session.close()


def main():
    """Función principal de pruebas"""
    print("🧪 PRUEBAS API VOLTIO - SERVIDOR DE PRODUCCIÓN")
    print("=" * 60)
    print(f"🕒 Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Pruebas básicas
    basic_results = test_basic_endpoints()
    
    # Pruebas de autenticación
    token = test_authentication()
    
    # Resumen final
    print(f"\n🏁 RESUMEN FINAL:")
    successful_basic = sum(1 for r in basic_results if r['success'])
    print(f"   📊 Endpoints básicos: {successful_basic}/{len(basic_results)} exitosos")
    print(f"   🔐 Autenticación: {'✅ Funciona' if token else '❌ Falló'}")
    
    overall_success = successful_basic >= len(basic_results) * 0.8 and token is not None
    if overall_success:
        print(f"\n🎉 ¡API VOLTIO está FUNCIONANDO en producción!")
    else:
        print(f"\n⚠️ API VOLTIO tiene algunos problemas en producción")
    
    print(f"\n🌐 URL de producción: {PROD_URL}")
    print(f"📚 Documentación: {PROD_URL}/docs")


if __name__ == "__main__":
    main()
