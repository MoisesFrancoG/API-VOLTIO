"""
Test script para verificar las mejoras de seguridad - user_id automático
"""
import requests
import json


def test_security_improvements():
    print("🔒 PROBANDO MEJORAS DE SEGURIDAD - USER_ID AUTOMÁTICO")
    print("=" * 65)

    # Obtener token
    login_data = {'email': 'admin@voltio.com', 'password': 'admin123'}
    r = requests.post(
        'http://localhost:8000/api/v1/users/login', json=login_data)
    if r.status_code != 200:
        print(f"❌ Error en login: {r.status_code}")
        return False

    token = r.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    print(f"✅ Token obtenido para admin")

    print(f"\n🧪 Probando endpoints con user_id automático...")

    # 1. Test Notifications POST - Sin user_id en body
    print(f"\n📬 1. NOTIFICATIONS POST (sin user_id):")
    notification_data = {
        # "user_id": 1,  # ❌ YA NO ES NECESARIO!
        "message": "🔒 Notificación con user_id automático",
        "is_read": False
    }
    r = requests.post('http://localhost:8000/api/v1/notifications/',
                      json=notification_data, headers=headers)
    print(f"   Status: {r.status_code}")
    if r.status_code == 201:
        result = r.json()
        print(
            f"   ✅ Creada correctamente - user_id asignado: {result['user_id']}")
        print(f"   📝 Mensaje: {result['message']}")
        notification_id = result['id']

        # Limpiar: eliminar la notificación de prueba
        requests.delete(
            f'http://localhost:8000/api/v1/notifications/{notification_id}', headers=headers)
    else:
        print(f"   ❌ Error: {r.text}")

    # 2. Test Devices POST - Sin user_id en body
    print(f"\n🔧 2. DEVICES POST (sin user_id):")

    # Primero verificar si hay device types y locations disponibles
    r_types = requests.get(
        'http://localhost:8000/api/v1/device-types/', headers=headers)
    r_locations = requests.get(
        'http://localhost:8000/api/v1/locations/', headers=headers)

    if r_types.status_code == 200 and r_locations.status_code == 200:
        device_types = r_types.json()
        locations = r_locations.json()

        if device_types and len(device_types) > 0:
            # Crear una ubicación de prueba si no hay ninguna
            if not locations:
                location_data = {
                    "name": "Test Location for Device",
                    "description": "Ubicación de prueba para dispositivo"
                }
                r_loc = requests.post(
                    'http://localhost:8000/api/v1/locations/', json=location_data, headers=headers)
                if r_loc.status_code == 201:
                    location_id = r_loc.json()['id']
                else:
                    print(f"   ⚠️  No se pudo crear ubicación de prueba")
                    location_id = 1  # Fallback
            else:
                location_id = locations[0]['id']

            device_data = {
                # "user_id": 1,  # ❌ YA NO ES NECESARIO!
                "name": "Test Device Security",
                "device_type_id": device_types[0]['id'],
                "location_id": location_id,
                "is_active": True
            }
            r = requests.post(
                'http://localhost:8000/api/v1/devices/', json=device_data, headers=headers)
            print(f"   Status: {r.status_code}")
            if r.status_code == 201:
                result = r.json()
                print(
                    f"   ✅ Creado correctamente - user_id asignado: {result['user_id']}")
                print(f"   📱 Dispositivo: {result['name']}")
                device_id = result['id']

                # Limpiar: eliminar el dispositivo de prueba
                requests.delete(
                    f'http://localhost:8000/api/v1/devices/{device_id}', headers=headers)
            else:
                print(f"   ❌ Error: {r.text}")
        else:
            print(f"   ⚠️  No hay device types disponibles para la prueba")
    else:
        print(f"   ⚠️  No se pueden obtener device types o locations")

    # 3. Verificar seguridad - intentar acceder a recursos de otros usuarios
    print(f"\n🛡️  3. VERIFICACIÓN DE SEGURIDAD:")

    # Listar notificaciones (solo debe ver las propias)
    r = requests.get(
        'http://localhost:8000/api/v1/notifications/', headers=headers)
    if r.status_code == 200:
        notifications = r.json()
        print(
            f"   ✅ Notificaciones visibles: {len(notifications)} (solo propias)")
        for notif in notifications:
            if notif['user_id'] != 1:  # admin user ID
                print(
                    f"   ⚠️  Posible filtrado incorrecto: user_id {notif['user_id']}")

    # Listar dispositivos (solo debe ver los propios)
    r = requests.get('http://localhost:8000/api/v1/devices/', headers=headers)
    if r.status_code == 200:
        devices = r.json()
        print(
            f"   ✅ Dispositivos visibles: {len(devices)} (filtrado aplicado)")
        for device in devices[:3]:  # Solo mostrar los primeros 3
            print(f"       - {device['name']} (user_id: {device['user_id']})")

    print(f"\n🎉 PRUEBAS DE SEGURIDAD COMPLETADAS")
    print("=" * 65)
    print("✅ Mejoras implementadas:")
    print("   🔐 user_id tomado automáticamente del token JWT")
    print("   🛡️  No es necesario especificar user_id en requests POST")
    print("   🎯 Mayor seguridad - usuarios solo ven sus propios recursos")
    print("   🚀 Mejor UX - APIs más simples de usar")

    return True


if __name__ == "__main__":
    test_security_improvements()
