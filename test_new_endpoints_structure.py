#!/usr/bin/env python3
"""
Test completo para los nuevos endpoints reorganizados de InfluxDB
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "https://voltioapi.acstree.xyz/api/v1"
TOKEN = None  # Se obtiene dinámicamente


def get_auth_token():
    """Obtiene el token de autenticación"""
    global TOKEN
    try:
        login_data = {
            "email": "admin@voltio.com",
            "password": "admin123"
        }
        response = requests.post(f"{BASE_URL}/users/login", json=login_data)
        if response.status_code == 200:
            TOKEN = response.json()["access_token"]
            print("✅ Token obtenido exitosamente")
            return True
        else:
            print(f"❌ Error obteniendo token: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Error en autenticación: {e}")
        return False


def test_endpoint(name, url, expected_status=200):
    """Test genérico para un endpoint"""
    if not TOKEN:
        print("❌ No hay token disponible")
        return False

    headers = {"Authorization": f"Bearer {TOKEN}"}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == expected_status:
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"✅ {name}: {len(data)} elementos")
                elif isinstance(data, dict) and 'total' in data:
                    print(f"✅ {name}: {data['total']} lecturas")
                else:
                    print(f"✅ {name}: Respuesta válida")
            else:
                print(f"✅ {name}: Status {response.status_code} (esperado)")
            return True
        else:
            print(
                f"❌ {name}: Status {response.status_code}, esperado {expected_status}")
            print(f"   Respuesta: {response.text[:200]}...")
            return False

    except Exception as e:
        print(f"❌ {name}: Error en request - {e}")
        return False


def main():
    """Función principal de testing"""
    print("🚀 === TESTING NUEVOS ENDPOINTS REORGANIZADOS ===")
    print("=" * 60)

    # Obtener token
    if not get_auth_token():
        print("❌ No se pudo obtener token. Abortando tests.")
        return

    # Definir endpoints a testear
    endpoints = [
        # Energy (PZEM) - Nuevos endpoints
        ("⚡ Energy Current", f"{BASE_URL}/energy/current"),
        ("⚡ Energy History 1h", f"{BASE_URL}/energy/history/1h"),
        ("⚡ Energy History 1d", f"{BASE_URL}/energy/history/1d"),
        ("⚡ Energy Devices", f"{BASE_URL}/energy/devices"),
        ("⚡ Energy with MAC", f"{BASE_URL}/energy/current?mac=PZEM-001"),
        ("⚡ Energy with DeviceId",
         f"{BASE_URL}/energy/current?deviceId=PZEM-DEV-001"),

        # Environment (DHT22) - Nuevos endpoints
        ("🌡️ Environment Current", f"{BASE_URL}/environment/current"),
        ("🌡️ Environment History 1h", f"{BASE_URL}/environment/history/1h"),
        ("🌡️ Environment History 1d", f"{BASE_URL}/environment/history/1d"),
        ("🌡️ Environment with MAC",
         f"{BASE_URL}/environment/current?mac=DHT22-001"),

        # Light - Nuevos endpoints
        ("💡 Light Current", f"{BASE_URL}/light/current"),
        ("💡 Light History 1h", f"{BASE_URL}/light/history/1h"),
        ("💡 Light History 1d", f"{BASE_URL}/light/history/1d"),
        ("💡 Light with MAC", f"{BASE_URL}/light/current?mac=LIGHT-001"),

        # Motion (PIR) - Nuevos endpoints
        ("🚶 Motion Current", f"{BASE_URL}/motion/current"),
        ("🚶 Motion Events 1h", f"{BASE_URL}/motion/events/1h"),
        ("🚶 Motion Events 1d", f"{BASE_URL}/motion/events/1d"),
        ("🚶 Motion with MAC", f"{BASE_URL}/motion/current?mac=PIR-001"),
    ]

    # Ejecutar tests
    successful = 0
    for name, url in endpoints:
        if test_endpoint(name, url):
            successful += 1

    # Resumen final
    print("\n" + "=" * 60)
    print("📊 === RESUMEN FINAL ===")

    total = len(endpoints)
    print(f"📈 Endpoints exitosos: {successful}/{total}")
    print(f"📊 Tasa de éxito: {(successful/total)*100:.1f}%")

    if successful == total:
        print("🎉 ¡TODOS LOS ENDPOINTS FUNCIONAN CORRECTAMENTE!")
    elif successful > total * 0.7:
        print("✅ La mayoría de endpoints funcionan correctamente")
    else:
        print("⚠️ Muchos endpoints necesitan atención")

    print(f"\n{'='*60}")
    print("🏁 Tests completados!")

    return successful == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
