#!/bin/bash
# Script de reparación de emergencia para el servidor
# Este script repara el requirements.txt corrupto y fuerza el redespliegue

echo "🔧 Iniciando reparación de emergencia..."

# 1. Hacer backup del requirements.txt corrupto
echo "📦 Creando backup del archivo corrupto..."
cp requirements.txt requirements.txt.corrupted.backup

# 2. Restaurar requirements.txt desde el repositorio
echo "📥 Descargando requirements.txt limpio desde GitHub..."
curl -o requirements.txt https://raw.githubusercontent.com/MoisesFrancoG/API-VOLTIO/develop/requirements.txt

# 3. Verificar que el archivo se descargó correctamente
echo "🔍 Verificando integridad del archivo..."
if grep -q "fastapi" requirements.txt; then
    echo "✅ requirements.txt restaurado correctamente"
else
    echo "❌ Error al descargar requirements.txt"
    exit 1
fi

# 4. Forzar instalación de dependencias
echo "📦 Instalando dependencias..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# 5. Verificar instalación
echo "🔍 Verificando instalación de FastAPI..."
python -c "import fastapi; print(f'FastAPI {fastapi.__version__} instalado correctamente')"

# 6. Reiniciar aplicación
echo "🔄 Reiniciando aplicación..."
sudo systemctl restart voltio-api 2>/dev/null || sudo supervisorctl restart voltio-api

# 7. Esperar y verificar
echo "⏳ Esperando que el servicio se inicie..."
sleep 10

# 8. Verificar endpoints
echo "🧪 Verificando endpoints..."
echo "Endpoint principal:"
curl -s http://localhost:8000/ | python -m json.tool

echo -e "\nProbando endpoint de prueba:"
curl -s http://localhost:8000/test/quick | python -m json.tool || echo "Endpoint de prueba aún no disponible"

echo "🎉 Reparación completada"
