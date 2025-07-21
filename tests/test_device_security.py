#!/usr/bin/env python3
"""
Test script for Device security improvements - automatic user_id handling
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000"


def get_auth_token():
    """Obtener token de autenticación"""
    login_data = {
        "email": "admin@voltio.com",
        "password": "admin123"
    }

    response = requests.post(f"{BASE_URL}/api/v1/users/login", json=login_data)

    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Token obtenido exitosamente")
        return token
    else:
        print(f"❌ Error obteniendo token: {response.status_code}")
        print(f"Response: {response.text}")
        return None


def test_create_device_with_security(token):
    """Test de creación de dispositivo con seguridad mejorada"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Primero crear una ubicación y tipo de dispositivo
    print("\n📝 Creating prerequisites (location and device type)...")

    # Crear ubicación
    location_data = {
        "name": "Test Location",
        "description": "Location for security test"
    }

    location_response = requests.post(f"{BASE_URL}/api/v1/locations/",
                                      headers=headers,
                                      json=location_data)

    if location_response.status_code != 200:
        print(f"❌ Error creating location: {location_response.text}")
        return None

    location_id = location_response.json()["id"]
    print(f"✅ Location created with ID: {location_id}")

    # Crear tipo de dispositivo
    device_type_data = {
        "name": "Test Device Type",
        "description": "Device type for security test"
    }

    device_type_response = requests.post(f"{BASE_URL}/api/v1/device-types/",
                                         headers=headers,
                                         json=device_type_data)

    if device_type_response.status_code != 200:
        print(f"❌ Error creating device type: {device_type_response.text}")
        return None

    device_type_id = device_type_response.json()["id"]
    print(f"✅ Device type created with ID: {device_type_id}")

    # Datos del dispositivo SIN user_id (debe tomarse del token)
    device_data = {
        "name": "Test Device Security",
        "device_type_id": device_type_id,
        "location_id": location_id,
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "description": "Device created with automatic user_id from JWT token",
        "is_active": True
    }

    print("\n📝 Testing Device Creation with Security Improvements...")
    print(
        f"Device data (without user_id): {json.dumps(device_data, indent=2)}")

    response = requests.post(f"{BASE_URL}/api/v1/devices/",
                             headers=headers,
                             json=device_data)

    print(f"\n📊 Response Status: {response.status_code}")

    if response.status_code == 200:
        device = response.json()
        print("✅ Device created successfully!")
        print(f"Created device: {json.dumps(device, indent=2)}")
        print(f"✅ User ID automatically set to: {device.get('user_id')}")
        print(f"✅ MAC address processed: {device.get('mac_address')}")
        print(f"✅ Description added: {device.get('description')}")
        return device['id']
    else:
        print(f"❌ Error creating device: {response.status_code}")
        print(f"Error details: {response.text}")
        return None


def test_get_device(token, device_id):
    """Test obtener dispositivo"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"\n📝 Testing Get Device {device_id}...")

    response = requests.get(
        f"{BASE_URL}/api/v1/devices/{device_id}", headers=headers)

    print(f"📊 Response Status: {response.status_code}")

    if response.status_code == 200:
        device = response.json()
        print("✅ Device retrieved successfully!")
        print(f"Device details: {json.dumps(device, indent=2)}")
    else:
        print(f"❌ Error getting device: {response.status_code}")
        print(f"Error details: {response.text}")


def main():
    """Función principal de testing"""
    print("🔧 Testing Device Module Security Improvements")
    print("=" * 50)

    # 1. Obtener token
    token = get_auth_token()
    if not token:
        return

    # 2. Test crear dispositivo con user_id automático
    device_id = test_create_device_with_security(token)

    # 3. Test obtener dispositivo
    if device_id:
        test_get_device(token, device_id)

    print("\n" + "=" * 50)
    print("🏁 Testing completed!")


if __name__ == "__main__":
    main()
