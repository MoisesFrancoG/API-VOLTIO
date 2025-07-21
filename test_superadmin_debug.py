#!/usr/bin/env python3
"""
Prueba específica del SuperAdmin y endpoint /users/me
"""

import requests
import json

BASE_URL = "https://voltioapi.acstree.xyz"
API_BASE = f"{BASE_URL}/api/v1"

def test_superadmin():
    print("🔐 Probando SuperAdmin específicamente...")
    
    # Login
    login_data = {
        "email": "superadmin@voltio.com",
        "password": "SuperAdmin123!"
    }
    
    session = requests.Session()
    
    try:
        # Login
        response = session.post(f"{API_BASE}/users/login", json=login_data, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Login falló: {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        data = response.json()
        token = data.get("access_token")
        
        if not token:
            print("❌ No se obtuvo token")
            return
            
        print(f"✅ Login exitoso! Token: {token[:30]}...")
        
        # Headers con token
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Probar /users/me
        print("\n📋 Probando /users/me...")
        me_response = session.get(f"{API_BASE}/users/me", headers=headers, timeout=10)
        print(f"Status: {me_response.status_code}")
        
        if me_response.status_code == 200:
            user_data = me_response.json()
            print(f"✅ Usuario: {user_data.get('email', 'N/A')}")
            print(f"✅ ID: {user_data.get('id', 'N/A')}")
            print(f"✅ Rol: {user_data.get('role_name', 'N/A')}")
            print(f"✅ Rol ID: {user_data.get('role_id', 'N/A')}")
        else:
            print(f"❌ /users/me falló: {me_response.text}")
            
        # Probar /roles con debugging
        print("\n📋 Probando /roles...")
        roles_response = session.get(f"{API_BASE}/roles", headers=headers, timeout=10)
        print(f"Status: {roles_response.status_code}")
        
        if roles_response.status_code == 200:
            roles = roles_response.json()
            print(f"✅ Roles encontrados: {len(roles)}")
            for role in roles[:3]:  # Mostrar primeros 3
                print(f"   - {role.get('role_name', 'N/A')} (ID: {role.get('id', 'N/A')})")
        else:
            print(f"❌ /roles falló: {roles_response.text}")
            
        # Probar crear un rol simple
        print("\n📋 Probando crear rol...")
        new_role = {
            "role_name": "Test Role Script",
            "description": "Rol de prueba desde script"
        }
        
        create_response = session.post(f"{API_BASE}/roles", headers=headers, json=new_role, timeout=10)
        print(f"Status: {create_response.status_code}")
        
        if create_response.status_code in [200, 201]:
            created_role = create_response.json()
            print(f"✅ Rol creado: {created_role.get('role_name', 'N/A')}")
        elif create_response.status_code == 409:
            print("⚠️ Rol ya existe (esperado)")
        else:
            print(f"❌ Crear rol falló: {create_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_superadmin()
