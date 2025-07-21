"""
Ejecutor de todos los tests para CI/CD
"""
import pytest
import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_basic_import():
    """Test básico de importación de módulos"""
    try:
        import src
        return True
    except ImportError as e:
        print(f"Error importando src: {e}")
        return False


def test_environment_setup():
    """Verificar configuración del entorno"""
    checks = {
        "main.py": (project_root / "main.py").exists(),
        "requirements.txt": (project_root / "requirements.txt").exists(),
        "src directory": (project_root / "src").exists(),
    }
    
    all_passed = True
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")
        if not result:
            all_passed = False
    
    return all_passed


def run_basic_tests():
    """Ejecutar tests básicos"""
    print("🧪 Ejecutando tests básicos para CI/CD...")
    print("=" * 50)
    
    tests = [
        ("Importación básica", test_basic_import),
        ("Configuración de entorno", test_environment_setup),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        try:
            if test_func():
                print(f"✅ {test_name} - PASÓ")
                passed += 1
            else:
                print(f"❌ {test_name} - FALLÓ")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    print(f"\n📊 Resultado: {passed}/{total} tests pasaron")
    return passed == total


if __name__ == "__main__":
    success = run_basic_tests()
    sys.exit(0 if success else 1)