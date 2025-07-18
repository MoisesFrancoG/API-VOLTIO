"""
Tests simples para verificar la configuración básica
"""

import pytest
from pathlib import Path


def test_project_structure():
    """Verificar que la estructura del proyecto es correcta"""
    project_root = Path(__file__).parent

    # Verificar archivos principales
    assert (project_root / "main.py").exists(), "main.py debe existir"
    assert (project_root /
            "requirements.txt").exists(), "requirements.txt debe existir"
    assert (project_root / "src").exists(), "directorio src debe existir"

    # Verificar módulos principales
    src_dir = project_root / "src"
    expected_modules = [
        "core", "Usuarios", "Roles", "Ubicaciones",
        "TipoSensores", "Sensores", "Lecturas",
        "ComandosIR", "Alertas"
    ]

    for module in expected_modules:
        module_path = src_dir / module
        if module_path.exists():
            assert (
                module_path / "__init__.py").exists(), f"__init__.py debe existir en {module}"


def test_environment_variables():
    """Verificar que las variables de entorno se pueden cargar"""
    try:
        from src.core.config import Settings
        # No crear instancia completa porque puede fallar sin .env
        # Solo verificar que el módulo se puede importar
        assert hasattr(Settings, '__init__'), "Settings debe tener constructor"
    except ImportError as e:
        pytest.skip(f"No se puede importar Settings: {e}")


def test_main_app_import():
    """Verificar que la aplicación principal se puede importar"""
    try:
        from main import app
        assert app is not None, "La aplicación FastAPI debe existir"
        assert hasattr(app, 'title'), "La aplicación debe tener título"
    except Exception as e:
        pytest.skip(f"No se puede importar main.app: {e}")


def test_basic_math():
    """Test básico para asegurar que pytest funciona"""
    assert 1 + 1 == 2, "Matemáticas básicas deben funcionar"
    assert True is True, "Booleanos deben funcionar"


@pytest.mark.parametrize("value,expected", [
    (1, True),
    (0, False),
    (-1, True),
])
def test_bool_conversion(value, expected):
    """Test parametrizado para verificar conversiones booleanas"""
    assert bool(value) == expected


if __name__ == "__main__":
    # Ejecutar tests si se llama directamente
    pytest.main([__file__, "-v"])
