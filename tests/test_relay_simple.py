"""
Script simplificado para probar el endpoint de comando de relé
"""
import requests
import json

# Configuración
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api/v1"

def main():
    print("🧪 Prueba simplificada del endpoint de relé")
    print("=" * 50)
    
    # Datos de prueba
    mac_address = "AA:BB:CC:DD:EE:FF"
    
    # 1. Prueba sin autenticación (debería fallar)
    print("\n1️⃣ Probando sin autenticación...")
    response = requests.post(
        f"{API_URL}/devices/{mac_address}/command/relay",
        json={"action": "ON"}
    )
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {response.text}")
    
    # 2. Prueba con token falso (debería fallar)
    print("\n2️⃣ Probando con token falso...")
    headers = {"Authorization": "Bearer fake_token"}
    response = requests.post(
        f"{API_URL}/devices/{mac_address}/command/relay",
        headers=headers,
        json={"action": "ON"}
    )
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {response.text}")
    
    # 3. Prueba con acción inválida
    print("\n3️⃣ Probando acción inválida...")
    response = requests.post(
        f"{API_URL}/devices/{mac_address}/command/relay",
        headers=headers,
        json={"action": "INVALID"}
    )
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {response.text}")
    
    print("\n✅ Pruebas básicas completadas")
    print("\nPara pruebas completas, necesitas:")
    print("- Usuario autenticado válido")
    print("- Dispositivo tipo NODO_CONTROL_PZEM registrado")
    print("- Conexión a RabbitMQ configurada")

if __name__ == "__main__":
    main()
