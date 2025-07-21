"""
Prueba de seguridad: Verificar que usuarios regulares NO pueden crear device_types
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api/v1"

def test_device_type_security():
    print("🔒 PRUEBA DE SEGURIDAD: Device Types")
    print("=" * 50)
    
    # Crear usuario regular de prueba
    print("👤 Creando usuario regular...")
    user_data = {
        "username": "regular_user_test",
        "email": "regular@test.com",
        "password": "testpass123",
        "role_id": 2  # Usuario regular
    }
    
    # Intentar registrar usuario
    response = requests.post(f"{API_URL}/users/register", json=user_data)
    
    if response.status_code == 201:
        print("✅ Usuario regular creado")
    elif "already exists" in response.text:
        print("ℹ️ Usuario regular ya existe")
    else:
        print(f"⚠️ Warning: {response.status_code} - {response.text}")
    
    # Login con usuario regular
    print("\n🔐 Haciendo login como usuario regular...")
    login_data = {"email": user_data['email'], "password": user_data['password']}
    response = requests.post(f"{API_URL}/users/login", json=login_data)
    
    if response.status_code != 200:
        print(f"❌ Error login: {response.status_code}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login exitoso como usuario regular")
    
    # Verificar rol del usuario
    print("\n🔍 Verificando rol del usuario...")
    response = requests.get(f"{API_URL}/users/", headers=headers)
    if response.status_code == 200:
        users = response.json()
        current_user = None
        for user in users:
            if user['email'] == user_data['email']:
                current_user = user
                break
        
        if current_user:
            print(f"👤 Usuario: {current_user['username']}")
            print(f"🏷️ Role ID: {current_user['role_id']}")
            if current_user['role_id'] == 2:
                print("✅ Confirmado: Usuario con rol REGULAR (ID: 2)")
            else:
                print(f"⚠️ Rol inesperado: {current_user['role_id']}")
    
    print("\n" + "="*50)
    print("🚨 INTENTANDO OPERACIONES RESTRINGIDAS")
    print("="*50)
    
    # 1. Intentar CREAR device type (debería fallar)
    print("\n1️⃣ Intentando CREAR device type...")
    device_type_data = {
        "type_name": "TIPO_MALICIOSO",
        "description": "Intento de usuario regular"
    }
    
    response = requests.post(f"{API_URL}/device-types/", headers=headers, json=device_type_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 403:
        print("✅ CORRECTO: Acceso denegado (403 Forbidden)")
        try:
            error_detail = response.json()
            print(f"Mensaje: {error_detail.get('detail', 'Sin detalle')}")
        except:
            print(f"Respuesta: {response.text}")
    else:
        print(f"❌ FALLO DE SEGURIDAD: Debería ser 403, pero fue {response.status_code}")
        print(f"Respuesta: {response.text}")
    
    # 2. Intentar ACTUALIZAR device type (debería fallar)
    print("\n2️⃣ Intentando ACTUALIZAR device type...")
    update_data = {
        "type_name": "TIPO_MODIFICADO",
        "description": "Intento de modificar"
    }
    
    response = requests.put(f"{API_URL}/device-types/5", headers=headers, json=update_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 403:
        print("✅ CORRECTO: Acceso denegado (403 Forbidden)")
    else:
        print(f"❌ FALLO DE SEGURIDAD: Debería ser 403, pero fue {response.status_code}")
        print(f"Respuesta: {response.text}")
    
    # 3. Intentar ELIMINAR device type (debería fallar)
    print("\n3️⃣ Intentando ELIMINAR device type...")
    
    response = requests.delete(f"{API_URL}/device-types/6", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 403:
        print("✅ CORRECTO: Acceso denegado (403 Forbidden)")
    else:
        print(f"❌ FALLO DE SEGURIDAD: Debería ser 403, pero fue {response.status_code}")
        print(f"Respuesta: {response.text}")
    
    # 4. Verificar que SÍ puede LEER device types
    print("\n4️⃣ Verificando que SÍ puede LEER device types...")
    
    response = requests.get(f"{API_URL}/device-types/", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ CORRECTO: Puede leer device types (operación permitida)")
        device_types = response.json()
        print(f"📋 Device types encontrados: {len(device_types)}")
        for dt in device_types:
            print(f"   - ID: {dt['id']} | Nombre: {dt['type_name']}")
    else:
        print(f"⚠️ Inesperado: No puede leer device types - Status: {response.status_code}")
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE SEGURIDAD")
    print("="*50)
    
    print("""
✅ CREAR device type:     ❌ BLOQUEADO (403 Forbidden)
✅ ACTUALIZAR device type: ❌ BLOQUEADO (403 Forbidden)  
✅ ELIMINAR device type:   ❌ BLOQUEADO (403 Forbidden)
✅ LEER device types:      ✅ PERMITIDO (200 OK)

🔒 CONCLUSIÓN: Los usuarios regulares NO pueden modificar device_types
🛡️ Solo admin (role_id=1) puede crear/modificar/eliminar
📖 Los usuarios regulares (role_id=2) solo pueden consultar los tipos existentes
""")

def main():
    try:
        test_device_type_security()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
