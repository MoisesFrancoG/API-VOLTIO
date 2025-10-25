#!/usr/bin/env python3
"""
Script para crear datos base necesarios para testing de dispositivos
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_colored(message, color):
    print(f"{color}{message}{Colors.END}")

def get_token():
    """Obtener token de autenticación"""
    login_data = {
        "email": "admin@voltio.com",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/users/login", json=login_data)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def create_device_types(token):
    """Crear tipos de dispositivos básicos"""
    headers = {"Authorization": f"Bearer {token}"}
    
    device_types = [
        {
            "type_name": "Sensor de Temperatura",
            "description": "Sensor para medir temperatura ambiente"
        },
        {
            "type_name": "Sensor de Humedad", 
            "description": "Sensor para medir humedad relativa"
        },
        {
            "type_name": "Medidor de Energía",
            "description": "Dispositivo para medir consumo eléctrico"
        }
    ]
    
    print_colored("📋 Creando tipos de dispositivos...", Colors.BLUE)
    
    for device_type in device_types:
        try:
            response = requests.post(f"{BASE_URL}/device-types/", json=device_type, headers=headers)
            print(f"Status: {response.status_code}, Response: {response.text}")
            
            if response.status_code == 201:
                created = response.json()
                print_colored(f"✅ Tipo creado: {created['type_name']} (ID: {created['id']})", Colors.GREEN)
            else:
                print_colored(f"❌ Error creando tipo: {device_type['type_name']}", Colors.RED)
        except Exception as e:
            print_colored(f"❌ Error: {e}", Colors.RED)

def create_locations(token):
    """Crear ubicaciones básicas"""
    headers = {"Authorization": f"Bearer {token}"}
    
    locations = [
        {
            "name": "Oficina Principal",
            "description": "Ubicación principal de la empresa",
            "address": "Calle Principal 123",
            "is_active": True
        },
        {
            "name": "Almacén", 
            "description": "Área de almacenamiento",
            "address": "Zona Industrial 456",
            "is_active": True
        },
        {
            "name": "Laboratorio",
            "description": "Laboratorio de pruebas",
            "address": "Edificio B, Piso 2",
            "is_active": True
        }
    ]
    
    print_colored("📍 Creando ubicaciones...", Colors.BLUE)
    
    for location in locations:
        try:
            response = requests.post(f"{BASE_URL}/locations/", json=location, headers=headers)
            print(f"Status: {response.status_code}, Response: {response.text}")
            
            if response.status_code == 201:
                created = response.json()
                print_colored(f"✅ Ubicación creada: {created['name']} (ID: {created['id']})", Colors.GREEN)
            else:
                print_colored(f"❌ Error creando ubicación: {location['name']}", Colors.RED)
        except Exception as e:
            print_colored(f"❌ Error: {e}", Colors.RED)

def list_existing_data(token):
    """Listar datos existentes"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print_colored("🔍 Verificando datos existentes...", Colors.YELLOW)
    
    # Tipos de dispositivos
    try:
        response = requests.get(f"{BASE_URL}/device-types/", headers=headers)
        print(f"Tipos de dispositivos - Status: {response.status_code}")
        if response.status_code == 200:
            types = response.json()
            print(f"Tipos encontrados: {len(types)}")
            for t in types:
                print(f"  - {t.get('type_name', 'N/A')} (ID: {t.get('id', 'N/A')})")
    except Exception as e:
        print(f"Error obteniendo tipos: {e}")
    
    # Ubicaciones
    try:
        response = requests.get(f"{BASE_URL}/locations/", headers=headers)
        print(f"Ubicaciones - Status: {response.status_code}")
        if response.status_code == 200:
            locations = response.json()
            print(f"Ubicaciones encontradas: {len(locations)}")
            for l in locations:
                print(f"  - {l.get('name', 'N/A')} (ID: {l.get('id', 'N/A')})")
    except Exception as e:
        print(f"Error obteniendo ubicaciones: {e}")

def main():
    print_colored("🚀 CONFIGURACIÓN DE DATOS BASE PARA TESTING", Colors.BLUE)
    print_colored("="*50, Colors.BLUE)
    
    token = get_token()
    if not token:
        print_colored("❌ No se pudo obtener token", Colors.RED)
        return
    
    print_colored("✅ Token obtenido", Colors.GREEN)
    
    # Listar datos existentes
    list_existing_data(token)
    
    # Crear tipos de dispositivos
    create_device_types(token)
    
    # Crear ubicaciones
    create_locations(token)
    
    # Verificar datos después de creación
    print_colored("\n🔄 Datos después de la creación:", Colors.YELLOW)
    list_existing_data(token)

if __name__ == "__main__":
    main()
