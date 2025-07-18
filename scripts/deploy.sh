#!/bin/bash
# Script para desplegar la aplicación manualmente

set -e  # Salir si hay algún error

echo "🚀 Iniciando despliegue de API Voltio..."

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ Error: No se encontró main.py. Asegúrate de estar en el directorio del proyecto."
    exit 1
fi

# Verificar que existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip e instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado. Copiando desde .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "📝 Por favor, edita el archivo .env con tus configuraciones:"
        echo "   nano .env"
        echo ""
        echo "❌ Configuración requerida antes de continuar."
        exit 1
    else
        echo "❌ No se encontró .env.example. Crea el archivo .env manualmente."
        exit 1
    fi
fi

# Ejecutar migraciones/creación de tablas
echo "🗄️  Ejecutando migraciones de base de datos..."
python -c "from src.core.db import engine, Base; Base.metadata.create_all(bind=engine); print('✅ Tablas creadas/actualizadas')"

# Verificar que la aplicación puede iniciarse
echo "🧪 Verificando configuración de la aplicación..."
python -c "
from src.core.config import Settings
settings = Settings()
print('✅ Configuración válida')
"

echo "✅ Despliegue preparado!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Configurar Supervisor: sudo cp configs/supervisor.conf /etc/supervisor/conf.d/voltio-api.conf"
echo "2. Configurar Nginx: sudo cp configs/nginx.conf /etc/nginx/sites-available/voltio-api"
echo "3. Activar sitio: sudo ln -s /etc/nginx/sites-available/voltio-api /etc/nginx/sites-enabled/"
echo "4. Reiniciar servicios:"
echo "   sudo supervisorctl reread && sudo supervisorctl update"
echo "   sudo systemctl restart nginx"
echo ""
echo "🌐 Para probar la aplicación localmente:"
echo "   source venv/bin/activate"
echo "   uvicorn main:app --host 0.0.0.0 --port 8000"
