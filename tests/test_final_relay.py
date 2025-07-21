"""
Prueba final del endpoint de relé con datos reales
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:8000'
API_URL = f'{BASE_URL}/api/v1'

def main():
    print("🔌 Prueba final del endpoint de comando de relé")
    print("=" * 50)
    
    # Login con el usuario que creamos
    print("🔐 Autenticando usuario...")
    login_data = {'email': 'relay_tester@example.com', 'password': 'testpass123'}
    response = requests.post(f'{API_URL}/users/login', json=login_data)
    
    if response.status_code == 200:
        token = response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        print("✅ Autenticación exitosa")
        
        # Probar con la MAC que sabemos que existe
        mac_address = "AA:BB:CC:DD:EE:FF"
        
        # 1. Probar comando ON
        print(f"\n1️⃣ Probando comando ON para dispositivo {mac_address}...")
        data = {"action": "ON"}
        response = requests.post(
            f'{API_URL}/devices/{mac_address}/command/relay',
            headers=headers,
            json=data
        )
        
        print(f"Status: {response.status_code}")
        try:
            print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except:
            print(f"Respuesta: {response.text}")
        
        # 2. Probar comando OFF
        print(f"\n2️⃣ Probando comando OFF para dispositivo {mac_address}...")
        data = {"action": "OFF"}
        response = requests.post(
            f'{API_URL}/devices/{mac_address}/command/relay',
            headers=headers,
            json=data
        )
        
        print(f"Status: {response.status_code}")
        try:
            print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except:
            print(f"Respuesta: {response.text}")
        
        # 3. Probar acción inválida
        print(f"\n3️⃣ Probando acción inválida...")
        data = {"action": "INVALID"}
        response = requests.post(
            f'{API_URL}/devices/{mac_address}/command/relay',
            headers=headers,
            json=data
        )
        
        print(f"Status: {response.status_code}")
        try:
            print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except:
            print(f"Respuesta: {response.text}")
            
    else:
        print(f"❌ Error en autenticación: {response.status_code}")
        print(f"Respuesta: {response.text}")

if __name__ == "__main__":
    main()
