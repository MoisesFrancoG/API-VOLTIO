#!/usr/bin/env python3
"""
Test completo de diagnóstico para dispositivos - Debug detallado
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    END = '\033[0m'

def print_colored(message, color):
    print(f"{color}{message}{Colors.END}")

def test_login():
    """Test login y obtener token"""
    print_colored("\n🔐 Probando login...", Colors.BLUE)
    
    login_data = {
        "email": "admin@voltio.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/login", json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print_colored("✅ Login exitoso", Colors.GREEN)
            return token
        else:
            print_colored("❌ Login falló", Colors.RED)
            return None
    except Exception as e:
        print_colored(f"❌ Error en login: {e}", Colors.RED)
        return None

def test_device_creation(token):
    """Test creación de dispositivo con debug detallado"""
    print_colored("\n📱 Probando creación de dispositivo...", Colors.BLUE)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Verificar primero que existan tipos y ubicaciones
    print_colored("🔍 Verificando tipos de dispositivos...", Colors.YELLOW)
    try:
        types_response = requests.get(f"{BASE_URL}/device-types/", headers=headers)
        print(f"Tipos Status: {types_response.status_code}")
        if types_response.status_code == 200:
            types = types_response.json()
            print(f"Tipos disponibles: {len(types)}")
            if types:
                print(f"Primer tipo: ID={types[0]['id']}, Name={types[0]['type_name']}")
    except Exception as e:
        print_colored(f"Error al obtener tipos: {e}", Colors.RED)
    
    print_colored("🔍 Verificando ubicaciones...", Colors.YELLOW)
    try:
        locations_response = requests.get(f"{BASE_URL}/locations/", headers=headers)
        print(f"Ubicaciones Status: {locations_response.status_code}")
        if locations_response.status_code == 200:
            locations = locations_response.json()
            print(f"Ubicaciones disponibles: {len(locations)}")
            if locations:
                print(f"Primera ubicación: ID={locations[0]['id']}, Name={locations[0]['name']}")
    except Exception as e:
        print_colored(f"Error al obtener ubicaciones: {e}", Colors.RED)
    
    # Probar varios casos de dispositivos con IDs válidos
    test_cases = [
        {
            "name": "Debug Device Test 1",
            "device_type_id": 17,  # NODO CONTROL ESP32
            "location_id": 13,     # Oficina
            "is_active": True,
            "mac_address": "AA:BB:CC:DD:EE:F1",
            "description": "Test device for debugging"
        },
        {
            "name": "Debug Device Test 2", 
            "device_type_id": 18,  # Sensor de Temperatura
            "location_id": 14,     # Sala de estar
            "is_active": True,
            "mac_address": "AA:BB:CC:DD:EE:F2",
            "description": "Temperature sensor test"
        },
        {
            "name": "Debug Device Test 3",
            "device_type_id": 19,  # Sensor de Humedad
            "location_id": 15,     # Comedor
            "is_active": True,
            "mac_address": "AA:BB:CC:DD:EE:F3",
            "description": "Humidity sensor test"
        }
    ]
    
    for i, device_data in enumerate(test_cases, 1):
        print_colored(f"\n📱 Test Case {i}: {device_data['name']}", Colors.PURPLE)
        print(f"Data: {json.dumps(device_data, indent=2)}")
        
        try:
            # Usar timeout más largo
            response = requests.post(
                f"{BASE_URL}/devices/", 
                json=device_data, 
                headers=headers,
                timeout=30  # 30 segundos timeout
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Response Text: {response.text}")
            
            if response.status_code == 201:
                device = response.json()
                print_colored(f"✅ Dispositivo creado: {device['name']} (ID: {device['id']})", Colors.GREEN)
                return device
            else:
                print_colored(f"❌ Error {response.status_code}: {response.text}", Colors.RED)
                
        except requests.exceptions.ConnectionError as e:
            print_colored(f"❌ Error de conexión: {e}", Colors.RED)
        except requests.exceptions.Timeout as e:
            print_colored(f"❌ Timeout: {e}", Colors.RED)
        except Exception as e:
            print_colored(f"❌ Error inesperado: {e}", Colors.RED)
    
    return None

def main():
    print_colored("🚀 DIAGNÓSTICO COMPLETO DE DISPOSITIVOS", Colors.BLUE)
    print_colored("="*50, Colors.BLUE)
    
    # Test login
    token = test_login()
    if not token:
        print_colored("❌ No se pudo obtener token, terminando", Colors.RED)
        sys.exit(1)
    
    # Test device creation
    device = test_device_creation(token)
    
    if device:
        print_colored("\n✅ DIAGNÓSTICO COMPLETADO - DISPOSITIVO CREADO", Colors.GREEN)
    else:
        print_colored("\n❌ DIAGNÓSTICO COMPLETADO - NO SE PUDO CREAR DISPOSITIVO", Colors.RED)

if __name__ == "__main__":
    main()
