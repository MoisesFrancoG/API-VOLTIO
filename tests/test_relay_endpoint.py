"""
Script de prueba para el endpoint de comando de relé
Prueba todos los casos de uso del endpoint /api/v1/devices/{mac_address}/command/relay
"""
import requests
import json
import sys
import os

# Configuración del servidor
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api/v1"

def get_auth_token():
    """Obtener token de autenticación"""
    print("🔐 Obteniendo token de autenticación...")
    
    # Intentar con usuario conocido
    login_data = {
        "email": "superadmin@gmail.com",
        "password": "superadmin123"
    }
    
    response = requests.post(f"{API_URL}/users/login", json=login_data)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Token obtenido exitosamente")
        return token
    else:
        print(f"❌ Error obteniendo token: {response.status_code}")
        print(f"Respuesta: {response.text}")
        return None

def test_relay_command(token, mac_address, action):
    """Probar comando de relé"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {"action": action}
    
    print(f"\n🔌 Enviando comando '{action}' a dispositivo {mac_address}...")
    
    response = requests.post(
        f"{API_URL}/devices/{mac_address}/command/relay",
        headers=headers,
        json=data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.status_code, response.json()

def test_device_not_found(token):
    """Probar con dispositivo que no existe"""
    fake_mac = "FF:FF:FF:FF:FF:FF"
    return test_relay_command(token, fake_mac, "ON")

def test_invalid_action(token, mac_address):
    """Probar con acción inválida"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {"action": "INVALID"}
    
    print(f"\n❌ Probando acción inválida para dispositivo {mac_address}...")
    
    response = requests.post(
        f"{API_URL}/devices/{mac_address}/command/relay",
        headers=headers,
        json=data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.status_code, response.json()

def get_user_devices(token):
    """Obtener dispositivos del usuario para las pruebas"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n📱 Obteniendo dispositivos del usuario...")
    
    response = requests.get(f"{API_URL}/devices/", headers=headers)
    
    if response.status_code == 200:
        devices = response.json()
        print(f"✅ Encontrados {len(devices)} dispositivos")
        
        for device in devices:
            print(f"  - ID: {device['id']} | Nombre: {device['name']} | MAC: {device.get('mac_address', 'N/A')} | Tipo: {device['device_type_id']}")
        
        return devices
    else:
        print(f"❌ Error obteniendo dispositivos: {response.status_code}")
        return []

def main():
    print("🚀 Iniciando pruebas del endpoint de comando de relé")
    print("=" * 60)
    
    # 1. Obtener token
    token = get_auth_token()
    if not token:
        print("❌ No se pudo obtener token. Terminando pruebas.")
        return
    
    # 2. Obtener dispositivos del usuario
    devices = get_user_devices(token)
    
    if not devices:
        print("⚠️ No hay dispositivos para probar. Creando dispositivo de prueba...")
        # Aquí podrías crear un dispositivo de prueba si es necesario
        return
    
    # 3. Buscar un dispositivo tipo NODO_CONTROL_PZEM (tipo 5)
    pzem_device = None
    for device in devices:
        if device['device_type_id'] == 5:  # NODO_CONTROL_PZEM
            pzem_device = device
            break
    
    if pzem_device:
        mac_address = pzem_device.get('mac_address')
        if mac_address:
            print(f"\n🎯 Dispositivo PZEM encontrado: {pzem_device['name']} ({mac_address})")
            
            # Pruebas con dispositivo válido
            print("\n" + "="*60)
            print("PRUEBAS CON DISPOSITIVO VÁLIDO")
            print("="*60)
            
            # Prueba 1: Comando ON
            test_relay_command(token, mac_address, "ON")
            
            # Prueba 2: Comando OFF  
            test_relay_command(token, mac_address, "OFF")
            
        else:
            print(f"⚠️ Dispositivo PZEM encontrado pero sin MAC address: {pzem_device['name']}")
    else:
        print("⚠️ No se encontró ningún dispositivo tipo NODO_CONTROL_PZEM para probar")
    
    # 4. Pruebas de errores
    print("\n" + "="*60)
    print("PRUEBAS DE CASOS DE ERROR")
    print("="*60)
    
    # Prueba 3: Dispositivo no encontrado
    test_device_not_found(token)
    
    # Prueba 4: Acción inválida
    if devices:
        test_invalid_action(token, devices[0].get('mac_address', 'AA:BB:CC:DD:EE:FF'))
    
    # Prueba 5: Dispositivo de tipo incorrecto
    non_pzem_device = None
    for device in devices:
        if device['device_type_id'] != 5:  # No es NODO_CONTROL_PZEM
            non_pzem_device = device
            break
    
    if non_pzem_device and non_pzem_device.get('mac_address'):
        print(f"\n🚫 Probando con dispositivo tipo incorrecto: {non_pzem_device['name']}")
        test_relay_command(token, non_pzem_device['mac_address'], "ON")
    
    print("\n🎉 Pruebas completadas!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
