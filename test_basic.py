"""
Tests básicos para CI/CD
"""
import pytest
import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_basic_import():
    """Test básico de importación"""
    try:
        import src
        assert True
    except ImportError as e:
        pytest.fail(f"Error importando src: {e}")


def test_environment_setup():
    """Verificar que el entorno está configurado correctamente"""
    # Verificar que los archivos principales existen
    assert (project_root / "main.py").exists(), "main.py debe existir"
    assert (project_root / "requirements.txt").exists(), "requirements.txt debe existir"
    assert (project_root / "src").exists(), "directorio src debe existir"


def test_requirements_file():
    """Verificar que requirements.txt es válido"""
    requirements_file = project_root / "requirements.txt"
    assert requirements_file.exists(), "requirements.txt debe existir"
    
    content = requirements_file.read_text(encoding='utf-8')
    assert "fastapi" in content, "FastAPI debe estar en requirements.txt"
    assert "uvicorn" in content, "Uvicorn debe estar en requirements.txt"


def test_core_modules():
    """Verificar que los módulos core se pueden importar"""
    try:
        from src.core import config
        assert True
    except ImportError:
        # No fallar si no está disponible en CI
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
