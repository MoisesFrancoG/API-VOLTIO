#!/usr/bin/env python3
"""
Test simple para diagnosticar el problema de creación de devices
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_device_creation():
    # 1. Login como admin
    login_data = {
        "email": "admin@voltio.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/login", json=login_data)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Token obtenido")
            
            # 2. Intentar crear device
            headers = {"Authorization": f"Bearer {token}"}
            device_data = {
                "name": "Test Device Simple",
                "device_type_id": 1,
                "location_id": 1,
                "is_active": True,
                "mac_address": "AA:BB:CC:DD:EE:22",
                "description": "Simple test device"
            }
            
            print(f"\n📝 Creando device...")
            print(f"Data: {json.dumps(device_data, indent=2)}")
            
            response = requests.post(f"{BASE_URL}/devices", json=device_data, headers=headers)
            print(f"\nCreate Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 201:
                print("✅ Device creado exitosamente!")
                device_id = response.json().get("id")
                print(f"Device ID: {device_id}")
                
                # 3. Verificar que se creó listando devices
                response = requests.get(f"{BASE_URL}/devices", headers=headers)
                print(f"\nList Status: {response.status_code}")
                devices = response.json()
                print(f"Total devices: {len(devices)}")
                
            else:
                print("❌ Error creando device")
                
        else:
            print("❌ Error en login")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_device_creation()
