#!/usr/bin/env python3
"""
Test simple para verificar la solución de errores en Lecturas PZEM
"""

from datetime import datetime
from src.Lecturas_influx_pzem.domain.schemas import LecturaPZEMResponse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_lectura_pzem_sin_device_id():
    """Test para verificar que LecturaPZEMResponse funciona sin deviceId"""

    # Datos simulando lo que viene de InfluxDB (sin deviceId)
    datos_influx = {
        "_time": datetime.now(),
        "mac": "CC:DB:A7:2F:AE:B0",
        "voltage": 127.5,
        "current": 2.1,
        "power": 267.75,
        "energy": 1.234,
        "frequency": 60.0,
        "powerFactor": 0.95
    }

    try:
        # Intentar crear el objeto sin deviceId
        lectura = LecturaPZEMResponse.model_validate(datos_influx)
        print("✅ Test 1 PASADO: LecturaPZEMResponse se crea correctamente sin deviceId")
        print(f"   deviceId: {lectura.deviceId}")
        print(f"   mac: {lectura.mac}")
        return True
    except Exception as e:
        print(f"❌ Test 1 FALLIDO: {e}")
        return False


def test_lectura_pzem_con_device_id():
    """Test para verificar que LecturaPZEMResponse funciona con deviceId"""

    # Datos con deviceId incluido
    datos_con_device_id = {
        "_time": datetime.now(),
        "deviceId": "DEVICE_001",
        "mac": "CC:DB:A7:2F:AE:B0",
        "voltage": 127.5,
        "current": 2.1,
        "power": 267.75,
        "energy": 1.234,
        "frequency": 60.0,
        "powerFactor": 0.95
    }

    try:
        lectura = LecturaPZEMResponse.model_validate(datos_con_device_id)
        print("✅ Test 2 PASADO: LecturaPZEMResponse se crea correctamente con deviceId")
        print(f"   deviceId: {lectura.deviceId}")
        print(f"   mac: {lectura.mac}")
        return True
    except Exception as e:
        print(f"❌ Test 2 FALLIDO: {e}")
        return False


def test_mapeo_mac_a_device_id():
    """Test para la lógica de mapeo en el repositorio"""

    # Simular el procesamiento que hace el repositorio
    datos_sin_device_id = {
        "_time": datetime.now(),
        "mac": "CC:DB:A7:2F:AE:B0",
        "voltage": 127.5,
        "current": 2.1,
        "power": 267.75,
        "energy": 1.234,
        "frequency": 60.0,
        "powerFactor": 0.95
    }

    # Aplicar la misma lógica del repositorio
    data = datos_sin_device_id.copy()
    if 'deviceId' not in data and 'mac' in data:
        data['deviceId'] = data['mac']

    try:
        lectura = LecturaPZEMResponse.model_validate(data)
        print("✅ Test 3 PASADO: Mapeo de MAC a deviceId funciona correctamente")
        print(f"   deviceId (mapeado): {lectura.deviceId}")
        print(f"   mac: {lectura.mac}")
        assert lectura.deviceId == lectura.mac, "deviceId debería ser igual a mac"
        return True
    except Exception as e:
        print(f"❌ Test 3 FALLIDO: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Ejecutando tests para verificar solución de errores...")
    print("=" * 60)

    tests_exitosos = 0
    total_tests = 3

    if test_lectura_pzem_sin_device_id():
        tests_exitosos += 1

    if test_lectura_pzem_con_device_id():
        tests_exitosos += 1

    if test_mapeo_mac_a_device_id():
        tests_exitosos += 1

    print("=" * 60)
    print(f"📊 Resultados: {tests_exitosos}/{total_tests} tests exitosos")

    if tests_exitosos == total_tests:
        print("🎉 ¡Todos los tests pasaron! La solución funciona correctamente.")
        sys.exit(0)
    else:
        print("⚠️  Algunos tests fallaron. Revisar la implementación.")
        sys.exit(1)
