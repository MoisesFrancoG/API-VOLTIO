"""
Tests para los nuevos endpoints de validación de despliegue
"""
import pytest
import requests
import json
from datetime import datetime


def test_deployment_v2_endpoint():
    """Test del nuevo endpoint de deployment v2"""
    response = requests.get("http://localhost:8000/test/deployment-v2")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "✅ Despliegue v2 funcionando"
    assert data["version"] == "1.2.0"
    assert "user_context" in data
    assert "git_info" in data
    assert "deployment_features" in data
    
    print("✅ Endpoint /test/deployment-v2 funcionando correctamente")


def test_system_info_endpoint():
    """Test del endpoint de información del sistema"""
    response = requests.get("http://localhost:8000/test/system-info")
    assert response.status_code == 200
    
    data = response.json()
    assert "server" in data
    assert "process" in data
    assert "directories" in data
    assert "network" in data
    assert "files" in data
    
    # Verificar campos específicos
    assert data["directories"]["project_exists"] == True
    assert data["directories"]["venv_active"] == True
    
    print("✅ Endpoint /test/system-info funcionando correctamente")


def test_database_check_endpoint():
    """Test del endpoint de verificación de bases de datos"""
    response = requests.get("http://localhost:8000/test/database-check")
    assert response.status_code == 200
    
    data = response.json()
    assert "databases" in data
    assert "postgresql" in data["databases"]
    assert "influxdb" in data["databases"]
    
    # Las conexiones pueden fallar en test, pero el endpoint debe responder
    for db in ["postgresql", "influxdb"]:
        assert "status" in data["databases"][db]
        assert "connection" in data["databases"][db]
    
    print("✅ Endpoint /test/database-check funcionando correctamente")


def test_environment_vars_endpoint():
    """Test del endpoint de variables de entorno"""
    response = requests.get("http://localhost:8000/test/environment-vars")
    assert response.status_code == 200
    
    data = response.json()
    assert "variables" in data
    assert "summary" in data
    assert data["summary"]["total_checked"] > 0
    
    # No debe mostrar valores completos de variables sensibles
    for var_name, var_info in data["variables"].items():
        if var_info.get("configured"):
            assert "preview" in var_info
            assert "*" in var_info["preview"]  # Debe estar censurado
    
    print("✅ Endpoint /test/environment-vars funcionando correctamente")


def test_api_performance_endpoint():
    """Test del endpoint de rendimiento"""
    response = requests.get("http://localhost:8000/test/api-performance")
    assert response.status_code == 200
    
    data = response.json()
    assert "results" in data
    assert "processing_time_seconds" in data["results"]
    assert "items_processed" in data["results"]
    assert "server_load" in data
    
    # El tiempo de procesamiento debe ser razonable
    assert data["results"]["processing_time_seconds"] < 5.0
    assert data["results"]["items_processed"] == 1000
    
    print("✅ Endpoint /test/api-performance funcionando correctamente")


def test_all_endpoints_summary():
    """Test del endpoint que lista todos los endpoints de test"""
    response = requests.get("http://localhost:8000/test/all-endpoints")
    assert response.status_code == 200
    
    data = response.json()
    assert "available_tests" in data
    assert "summary" in data
    assert data["summary"]["total_endpoints"] >= 8
    assert data["summary"]["new_endpoints"] >= 5
    
    # Verificar que todos los endpoints listados existen
    expected_endpoints = [
        "/test/quick",
        "/test/health", 
        "/test/deployment",
        "/test/deployment-v2",
        "/test/system-info",
        "/test/database-check",
        "/test/environment-vars",
        "/test/api-performance"
    ]
    
    listed_endpoints = [test["endpoint"] for test in data["available_tests"]]
    for endpoint in expected_endpoints:
        assert endpoint in listed_endpoints, f"Endpoint {endpoint} no está listado"
    
    print("✅ Endpoint /test/all-endpoints funcionando correctamente")


def test_all_new_endpoints_respond():
    """Test para verificar que todos los nuevos endpoints responden correctamente"""
    new_endpoints = [
        "/test/deployment-v2",
        "/test/system-info", 
        "/test/database-check",
        "/test/environment-vars",
        "/test/api-performance",
        "/test/all-endpoints"
    ]
    
    failed_endpoints = []
    
    for endpoint in new_endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}")
            if response.status_code != 200:
                failed_endpoints.append(f"{endpoint} - Status: {response.status_code}")
        except Exception as e:
            failed_endpoints.append(f"{endpoint} - Error: {str(e)}")
    
    if failed_endpoints:
        pytest.fail(f"Endpoints fallidos: {failed_endpoints}")
    
    print("✅ Todos los nuevos endpoints responden correctamente")


def test_deployment_version_change():
    """Verificar que la versión cambió para confirmar nuevos despliegues"""
    
    # Test endpoint v1
    response_v1 = requests.get("http://localhost:8000/test/deployment")
    data_v1 = response_v1.json()
    
    # Test endpoint v2  
    response_v2 = requests.get("http://localhost:8000/test/deployment-v2")
    data_v2 = response_v2.json()
    
    # Las versiones deben ser diferentes
    assert data_v1["version"] != data_v2["version"]
    assert data_v2["version"] == "1.2.0"
    
    print(f"✅ Versiones diferentes: v1={data_v1['version']}, v2={data_v2['version']}")


if __name__ == "__main__":
    """Ejecutar tests individuales para verificación rápida"""
    print("🧪 Ejecutando tests de nuevos endpoints...")
    
    try:
        test_deployment_v2_endpoint()
        test_system_info_endpoint()
        test_database_check_endpoint()
        test_environment_vars_endpoint()
        test_api_performance_endpoint() 
        test_all_endpoints_summary()
        test_all_new_endpoints_respond()
        test_deployment_version_change()
        
        print("\n🎉 Todos los tests pasaron exitosamente!")
        print("📊 Resumen:")
        print("- 8 endpoints de test funcionando")
        print("- 5 nuevos endpoints agregados")
        print("- Versión actualizada a 1.2.0")
        print("- Validación de despliegue completa")
        
    except Exception as e:
        print(f"\n❌ Error en los tests: {str(e)}")
        exit(1)
