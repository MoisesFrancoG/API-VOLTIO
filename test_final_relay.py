"""
Prueba final del endpoint de relé con datos reales - Versión robusta
"""
import requests
import json
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = 'http://127.0.0.1:8000'
API_URL = f'{BASE_URL}/api/v1'


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


def main():
    print("🔌 Prueba final del endpoint de comando de relé - ROBUSTA")
    print("=" * 60)

    session = create_robust_session()

    # Login con el superadmin
    print("🔐 Autenticando con superadmin...")
    login_data = {'email': 'superadmin@voltio.com',
                  'password': 'SuperAdmin123!'}
    
    try:
        response = session.post(f'{API_URL}/users/login', json=login_data, timeout=10)
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Tip: Asegúrate de que la API esté ejecutándose")
        return

    if response.status_code == 200:
        token = response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        print("✅ Autenticación exitosa")

        # Probar con la MAC que sabemos que existe
        mac_address = "AA:BB:CC:DD:EE:F1"

        # 1. Probar comando ON
        print(f"\n1️⃣ Probando comando ON para dispositivo {mac_address}...")
        data = {"action": "ON"}
        try:
            response = session.post(
                f'{API_URL}/devices/{mac_address}/command/relay',
                headers=headers,
                json=data,
                timeout=10
            )
            print(f"Status: {response.status_code}")
            try:
                print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            except:
                print(f"Respuesta: {response.text}")
        except Exception as e:
            print(f"❌ Error en comando ON: {e}")

        # 2. Probar comando OFF
        print(f"\n2️⃣ Probando comando OFF para dispositivo {mac_address}...")
        data = {"action": "OFF"}
        try:
            response = session.post(
                f'{API_URL}/devices/{mac_address}/command/relay',
                headers=headers,
                json=data,
                timeout=10
            )
            print(f"Status: {response.status_code}")
            try:
                print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            except:
                print(f"Respuesta: {response.text}")
        except Exception as e:
            print(f"❌ Error en comando OFF: {e}")

        # 3. Probar acción inválida
        print(f"\n3️⃣ Probando acción inválida...")
        data = {"action": "INVALID"}
        try:
            response = session.post(
                f'{API_URL}/devices/{mac_address}/command/relay',
                headers=headers,
                json=data,
                timeout=10
            )
            print(f"Status: {response.status_code}")
            try:
                print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            except:
                print(f"Respuesta: {response.text}")
        except Exception as e:
            print(f"❌ Error en comando INVALID: {e}")

    else:
        print(f"❌ Error en autenticación: {response.status_code}")
        try:
            print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except:
            print(f"Respuesta: {response.text}")
    
    print(f"\n🏁 Prueba completada!")
    session.close()


if __name__ == "__main__":
    main()
