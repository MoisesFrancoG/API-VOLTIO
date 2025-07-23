#!/usr/bin/env python3
"""
Script para diagnosticar y corregir errores específicos en endpoints de devices
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_colored(message, color):
    print(f"{color}{message}{Colors.END}")

def get_admin_token():
    """Obtener token de admin"""
    login_data = {
        "email": "admin@voltio.com",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/users/login", json=login_data)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def diagnose_endpoint_errors():
    """Diagnosticar errores específicos en endpoints"""
    
    token = get_admin_token()
    if not token:
        print_colored("❌ No se pudo obtener token", Colors.RED)
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print_colored("🔍 DIAGNÓSTICO DE ERRORES EN ENDPOINTS", Colors.BLUE)
    print_colored("="*50, Colors.BLUE)
    
    # 1. ERROR 400 en POST /devices para Regular User y SuperAdmin
    print_colored("\n1. INVESTIGANDO: Error 400 en POST /devices", Colors.YELLOW)
    print_colored("-"*40, Colors.YELLOW)
    
    # Verificar qué devuelve el endpoint cuando falla
    test_device = {
        "name": "Test Device Error Debug",
        "device_type_id": 17,
        "location_id": 13,
        "is_active": True,
        "mac_address": "AA:BB:CC:DD:EE:F9",
        "description": "Debug error device"
    }
    
    # Probar con usuario regular
    regular_login = {
        "email": "roletest@voltio.com",
        "password": "roletest123"
    }
    
    try:
        regular_response = requests.post(f"{BASE_URL}/users/login", json=regular_login)
        if regular_response.status_code == 200:
            regular_token = regular_response.json().get("access_token")
            regular_headers = {"Authorization": f"Bearer {regular_token}"}
            
            create_response = requests.post(f"{BASE_URL}/devices/", json=test_device, headers=regular_headers)
            print(f"Regular User POST /devices:")
            print(f"  Status: {create_response.status_code}")
            print(f"  Response: {create_response.text}")
        else:
            print("❌ No se pudo autenticar usuario regular")
    except Exception as e:
        print(f"❌ Error probando Regular User: {e}")
    
    # 2. ERROR 400 en PUT /devices para todos los usuarios  
    print_colored("\n2. INVESTIGANDO: Error 400 en PUT /devices", Colors.YELLOW)
    print_colored("-"*40, Colors.YELLOW)
    
    # Primero crear un device para luego actualizarlo
    create_response = requests.post(f"{BASE_URL}/devices/", json=test_device, headers=headers)
    if create_response.status_code == 201:
        device_id = create_response.json().get("id")
        print(f"✅ Device creado para test: ID {device_id}")
        
        update_data = {
            "name": "Updated Device Name",
            "description": "Updated description"
        }
        
        update_response = requests.put(f"{BASE_URL}/devices/{device_id}", json=update_data, headers=headers)
        print(f"PUT /devices/{device_id}:")
        print(f"  Status: {update_response.status_code}")
        print(f"  Response: {update_response.text}")
        
        # Limpiar - eliminar el device creado
        requests.delete(f"{BASE_URL}/devices/{device_id}", headers=headers)
    else:
        print("❌ No se pudo crear device para test de UPDATE")
    
    # 3. ERROR 400 en GET /devices/user/{user_id} para Admin
    print_colored("\n3. INVESTIGANDO: Error 400 en GET /devices/user/", Colors.YELLOW)
    print_colored("-"*40, Colors.YELLOW)
    
    # Obtener info del usuario admin
    me_response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    if me_response.status_code == 200:
        user_info = me_response.json()
        user_id = user_info.get("id")
        print(f"Admin user ID: {user_id}")
        
        devices_response = requests.get(f"{BASE_URL}/devices/user/{user_id}", headers=headers)
        print(f"GET /devices/user/{user_id}:")
        print(f"  Status: {devices_response.status_code}")
        print(f"  Response: {devices_response.text}")
    else:
        print("❌ No se pudo obtener info del usuario admin")
    
    # 4. ERROR 422 en GET /devices/search
    print_colored("\n4. INVESTIGANDO: Error 422 en GET /devices/search", Colors.YELLOW)
    print_colored("-"*40, Colors.YELLOW)
    
    # Probar diferentes formatos de búsqueda
    search_variants = [
        "/devices/search/?q=test",
        "/devices/search?q=test", 
        "/devices/search/test",
        "/devices/search"
    ]
    
    for search_url in search_variants:
        try:
            search_response = requests.get(f"{BASE_URL}{search_url}", headers=headers)
            print(f"GET {search_url}:")
            print(f"  Status: {search_response.status_code}")
            print(f"  Response: {search_response.text[:200]}")
        except Exception as e:
            print(f"❌ Error en {search_url}: {e}")
    
    # 5. Verificar estructura de endpoints disponibles
    print_colored("\n5. VERIFICANDO: Estructura de endpoints de devices", Colors.YELLOW)
    print_colored("-"*40, Colors.YELLOW)
    
    # Obtener la documentación de la API
    try:
        docs_response = requests.get(f"http://localhost:8000/docs")
        print(f"Docs disponibles: Status {docs_response.status_code}")
        
        # Verificar endpoints raíz
        root_response = requests.get(f"http://localhost:8000/")
        print(f"Root endpoint: Status {root_response.status_code}")
        
    except Exception as e:
        print(f"❌ Error verificando docs: {e}")

def main():
    diagnose_endpoint_errors()

if __name__ == "__main__":
    main()
