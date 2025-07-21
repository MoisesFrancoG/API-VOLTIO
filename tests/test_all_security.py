"""
Prueba de seguridad completa: Verificar todos los endpoints administrativos
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api/v1"

def test_all_admin_endpoints():
    print("🔒 PRUEBA DE SEGURIDAD COMPLETA")
    print("=" * 60)
    
    # Login como usuario regular
    print("🔐 Haciendo login como usuario regular...")
    login_data = {"email": "regular@test.com", "password": "testpass123"}
    response = requests.post(f"{API_URL}/users/login", json=login_data)
    
    if response.status_code != 200:
        print(f"❌ Error login: {response.status_code}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login exitoso como usuario regular")
    
    print("\n🚨 PROBANDO ENDPOINTS ADMINISTRATIVOS")
    print("=" * 60)
    
    # 1. TEST ROLES
    print("\n1️⃣ TESTING ROLES:")
    print("-" * 30)
    
    # Crear rol
    role_data = {"role_name": "ROL_MALICIOSO", "description": "Intento de usuario regular"}
    response = requests.post(f"{API_URL}/roles/", headers=headers, json=role_data)
    print(f"CREATE rol - Status: {response.status_code}")
    if response.status_code == 403:
        print("✅ CORRECTO: Bloqueado")
    else:
        print(f"❌ FALLO: Debería ser 403, fue {response.status_code}")
        print(f"Respuesta: {response.text[:100]}...")
    
    # Actualizar rol
    update_data = {"role_name": "ROL_MODIFICADO", "description": "Intento de modificar"}
    response = requests.put(f"{API_URL}/roles/1", headers=headers, json=update_data)
    print(f"UPDATE rol - Status: {response.status_code}")
    if response.status_code == 403:
        print("✅ CORRECTO: Bloqueado")
    else:
        print(f"❌ FALLO: Debería ser 403, fue {response.status_code}")
        print(f"Respuesta: {response.text[:100]}...")
    
    # 2. TEST UBICACIONES
    print("\n2️⃣ TESTING UBICACIONES:")
    print("-" * 30)
    
    # Crear ubicación
    location_data = {"name": "UBICACION_MALICIOSA", "description": "Intento de usuario regular"}
    response = requests.post(f"{API_URL}/locations/", headers=headers, json=location_data)
    print(f"CREATE ubicación - Status: {response.status_code}")
    if response.status_code == 403:
        print("✅ CORRECTO: Bloqueado")
    else:
        print(f"❌ FALLO: Debería ser 403, fue {response.status_code}")
        print(f"Respuesta: {response.text[:100]}...")
    
    # Actualizar ubicación
    update_data = {"name": "UBICACION_MODIFICADA", "description": "Intento de modificar"}
    response = requests.put(f"{API_URL}/locations/1", headers=headers, json=update_data)
    print(f"UPDATE ubicación - Status: {response.status_code}")
    if response.status_code == 403:
        print("✅ CORRECTO: Bloqueado")
    else:
        print(f"❌ FALLO: Debería ser 403, fue {response.status_code}")
        print(f"Respuesta: {response.text[:100]}...")
    
    # 3. TEST COMANDOS IR
    print("\n3️⃣ TESTING COMANDOS IR:")
    print("-" * 30)
    
    # Crear comando IR
    ir_data = {
        "device_name": "DISPOSITIVO_MALICIOSO",
        "command_name": "COMANDO_MALICIOSO",
        "ir_code": "FF00FF00",
        "description": "Intento de usuario regular"
    }
    response = requests.post(f"{API_URL}/device-commands/", headers=headers, json=ir_data)
    print(f"CREATE comando IR - Status: {response.status_code}")
    if response.status_code == 403:
        print("✅ CORRECTO: Bloqueado")
    else:
        print(f"❌ FALLO: Debería ser 403, fue {response.status_code}")
        print(f"Respuesta: {response.text[:100]}...")
    
    # 4. TEST DEVICE TYPES (ya corregido)
    print("\n4️⃣ TESTING DEVICE TYPES (Corregido):")
    print("-" * 30)
    
    device_type_data = {"type_name": "TIPO_MALICIOSO2", "description": "Verificar corrección"}
    response = requests.post(f"{API_URL}/device-types/", headers=headers, json=device_type_data)
    print(f"CREATE device type - Status: {response.status_code}")
    if response.status_code == 403:
        print("✅ CORRECTO: Bloqueado (ya corregido)")
    else:
        print(f"❌ FALLO: Debería ser 403, fue {response.status_code}")
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE SEGURIDAD")
    print("=" * 60)
    print("""
🔒 ESTADO ACTUAL:
   ✅ Device Types: CORREGIDO (solo admin)
   ❓ Roles: POR VERIFICAR
   ❓ Ubicaciones: POR VERIFICAR  
   ❓ Comandos IR: POR VERIFICAR
   
🛡️ RECOMENDACIÓN:
   Solo admin (role_id=1) debería poder modificar datos maestros
   Usuarios regulares (role_id=2) solo lectura/uso
    """)

if __name__ == "__main__":
    test_all_admin_endpoints()
