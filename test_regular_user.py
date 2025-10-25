#!/usr/bin/env python3
"""
Test específico para verificar usuario regular
"""

import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_regular_user():
    """Test específico para usuario regular"""
    
    print("🔍 Verificando usuario regular...")
    
    login_data = {
        "email": "roletest@voltio.com",
        "password": "roletest123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/login", json=login_data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("✅ Usuario regular autenticado exitosamente")
            
            # Probar crear un device
            headers = {"Authorization": f"Bearer {token}"}
            device_data = {
                "name": "Test Regular User Device",
                "device_type_id": 17,
                "location_id": 13,
                "is_active": True,
                "mac_address": "EE:FF:00:11:22:33",
                "description": "Device from regular user"
            }
            
            create_response = requests.post(f"{BASE_URL}/devices/", json=device_data, headers=headers, timeout=10)
            print(f"Create device - Status: {create_response.status_code}")
            print(f"Create response: {create_response.text}")
            
            if create_response.status_code == 201:
                device = create_response.json()
                device_id = device["id"]
                print(f"✅ Device creado por usuario regular: ID {device_id}")
                
                # Cleanup
                delete_response = requests.delete(f"{BASE_URL}/devices/{device_id}", headers=headers)
                print(f"Delete status: {delete_response.status_code}")
            
        else:
            print("❌ Error autenticando usuario regular")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_regular_user()
