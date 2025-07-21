"""
Script para probar la integración real con tu ESP32
Usa la MAC real de tu dispositivo para enviar comandos
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api/v1"

def test_esp32_integration():
    print("🔌 PRUEBA DE INTEGRACIÓN REAL CON ESP32")
    print("=" * 50)
    
    # Configuración (actualiza con tus datos reales)
    esp32_mac = input("📱 Ingresa la MAC de tu ESP32 (formato AA:BB:CC:DD:EE:FF): ").strip()
    
    if not esp32_mac:
        print("❌ MAC requerida para continuar")
        return
    
    print(f"🎯 Dispositivo objetivo: {esp32_mac}")
    
    # Login (actualiza con tus credenciales)
    print("\n🔐 Autenticando...")
    
    email = input("📧 Email del usuario (o presiona Enter para usar relay_tester@example.com): ").strip()
    if not email:
        email = "relay_tester@example.com"
    
    password = input("🔑 Password (o presiona Enter para usar testpass123): ").strip()
    if not password:
        password = "testpass123"
    
    login_data = {"email": email, "password": password}
    response = requests.post(f"{API_URL}/users/login", json=login_data)
    
    if response.status_code != 200:
        print(f"❌ Error de autenticación: {response.status_code}")
        print("💡 Asegúrate de tener un usuario válido o crea uno primero")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Autenticación exitosa")
    
    # Verificar si el dispositivo existe
    print(f"\n🔍 Verificando si existe dispositivo {esp32_mac}...")
    
    # Buscar dispositivo por MAC
    response = requests.get(f"{API_URL}/devices/", headers=headers)
    device_exists = False
    device_info = None
    
    if response.status_code == 200:
        devices = response.json()
        for device in devices:
            if device.get('mac_address') == esp32_mac:
                device_exists = True
                device_info = device
                break
    
    if device_exists:
        print(f"✅ Dispositivo encontrado: {device_info['name']}")
        print(f"   Tipo: {device_info['device_type_id']}")
        print(f"   Activo: {device_info['is_active']}")
        
        if device_info['device_type_id'] != 5:
            print("⚠️ ADVERTENCIA: El dispositivo no es tipo NODO_CONTROL_PZEM (tipo 5)")
            print("   Los comandos podrían fallar por validación de tipo")
    else:
        print("❌ Dispositivo no encontrado en la base de datos")
        print("💡 Necesitas crear el dispositivo primero con:")
        print(f"   - MAC: {esp32_mac}")
        print(f"   - Tipo: NODO_CONTROL_PZEM (ID: 5)")
        print(f"   - Usuario: {email}")
        return
    
    # Instrucciones para ESP32
    print(f"\n📋 PREPARACIÓN DEL ESP32:")
    print("=" * 40)
    print("1. ✅ Conecta tu ESP32 y abre el Serial Monitor")
    print("2. ✅ Verifica que esté en estado 'STATE_OPERATING' (LED fijo)")
    print("3. ✅ Confirma que muestre 'conectado!' en MQTT")
    print(f"4. ✅ Verifica que la MAC mostrada sea: {esp32_mac}")
    print(f"5. ✅ El topic de comando debe ser: pzem/command/{esp32_mac}")
    
    input("\n⏳ Presiona Enter cuando tu ESP32 esté listo...")
    
    # Pruebas de comandos
    print(f"\n🚀 ENVIANDO COMANDOS AL ESP32")
    print("=" * 40)
    
    def send_command(action, delay_after=3):
        print(f"\n🔌 Enviando comando '{action}'...")
        data = {"action": action}
        
        response = requests.post(
            f"{API_URL}/devices/{esp32_mac}/command/relay",
            headers=headers,
            json=data
        )
        
        print(f"📡 Status API: {response.status_code}")
        
        if response.status_code == 202:
            print("✅ Comando enviado exitosamente!")
            print("👀 Revisa tu ESP32 - el relé debería cambiar de estado")
            print("📺 Verifica el Serial Monitor para confirmar recepción")
        else:
            print(f"❌ Error: {response.text}")
        
        if delay_after > 0:
            print(f"⏳ Esperando {delay_after} segundos...")
            time.sleep(delay_after)
        
        return response.status_code == 202
    
    # Secuencia de pruebas
    print("🔥 Iniciando secuencia de pruebas...")
    
    # Comando ON
    success1 = send_command("ON", 5)
    
    # Comando OFF
    success2 = send_command("OFF", 5)
    
    # Comando ON nuevamente
    success3 = send_command("ON", 3)
    
    # Comando OFF final
    success4 = send_command("OFF", 0)
    
    # Resumen
    print(f"\n📊 RESUMEN DE PRUEBAS:")
    print("=" * 30)
    print(f"ON #1:  {'✅' if success1 else '❌'}")
    print(f"OFF #1: {'✅' if success2 else '❌'}")
    print(f"ON #2:  {'✅' if success3 else '❌'}")
    print(f"OFF #2: {'✅' if success4 else '❌'}")
    
    if all([success1, success2, success3, success4]):
        print("\n🎉 ¡INTEGRACIÓN COMPLETAMENTE FUNCIONAL!")
        print("🔗 La API y tu ESP32 están comunicándose perfectamente")
    else:
        print("\n⚠️ Algunas pruebas fallaron")
        print("🔧 Revisa la conexión MQTT de tu ESP32")
    
    print(f"\n💡 TIP: Puedes usar la documentación interactiva en:")
    print(f"   {BASE_URL}/docs")

if __name__ == "__main__":
    try:
        test_esp32_integration()
    except KeyboardInterrupt:
        print("\n\n⚠️ Prueba interrumpida")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
