#!/bin/bash
# Script universal para solucionar problemas de despliegue en EC2

echo "🔧 Iniciando solución de problemas de despliegue..."
echo "👤 Usuario actual: $(whoami)"
echo "🏠 Directorio home: $HOME"

# Función para encontrar el directorio del proyecto
find_project_dir() {
    local possible_dirs=(
        "/home/deploy/API-VOLTIO"
        "/home/ubuntu/API-VOLTIO" 
        "$HOME/API-VOLTIO"
        "/opt/API-VOLTIO"
        "/var/www/API-VOLTIO"
    )
    
    for dir in "${possible_dirs[@]}"; do
        if [ -d "$dir" ]; then
            echo "✅ Directorio del proyecto encontrado: $dir"
            echo "$dir"
            return 0
        fi
    done
    
    echo "🔍 Buscando en todo el sistema..."
    local found_dir=$(find /home /opt /var -name "API-VOLTIO" -type d 2>/dev/null | head -1)
    if [ -n "$found_dir" ]; then
        echo "✅ Directorio encontrado: $found_dir"
        echo "$found_dir"
        return 0
    fi
    
    echo "❌ No se encontró el directorio API-VOLTIO"
    return 1
}

# Encontrar el directorio del proyecto
PROJECT_DIR=$(find_project_dir)
if [ -z "$PROJECT_DIR" ]; then
    echo "❌ No se puede continuar sin el directorio del proyecto"
    exit 1
fi

# Cambiar al directorio del proyecto
cd "$PROJECT_DIR" || {
    echo "❌ No se puede acceder a $PROJECT_DIR"
    exit 1
}

echo "📁 Trabajando en: $(pwd)"

# Verificar permisos
if [ ! -w "." ]; then
    echo "⚠️  Sin permisos de escritura. Intentando con sudo..."
    if [ "$(whoami)" != "root" ]; then
        echo "🔄 Reejecutando con sudo..."
        sudo bash "$0"
        exit $?
    fi
fi

echo "📋 Contenido del directorio:"
ls -la

# Verificar git
if [ -d ".git" ]; then
    echo "✅ Repositorio git encontrado"
    echo "📋 Estado de Git:"
    git status --porcelain || {
        echo "⚠️  Error con git, continuando..."
    }
else
    echo "❌ No es un repositorio git"
fi

# Solución 1: Stash cambios locales si existen
echo "💾 Guardando cambios locales..."
if git diff --quiet && git diff --staged --quiet 2>/dev/null; then
    echo "✅ No hay cambios locales pendientes"
else
    echo "⚠️  Hay cambios locales. Guardándolos..."
    git stash push -m "Cambios locales antes de pull $(date)" 2>/dev/null || echo "Error con git stash, continuando..."
fi

# Solución 2: Actualizar código
echo "⬇️  Actualizando código desde GitHub..."
git pull origin develop 2>/dev/null || {
    echo "⚠️  Error con git pull, intentando reset..."
    git fetch origin develop 2>/dev/null
    git reset --hard origin/develop 2>/dev/null || echo "Error con git, continuando..."
}

# Solución 3: Verificar y activar entorno virtual
echo "🐍 Verificando entorno virtual..."
if [ -d "venv" ]; then
    echo "✅ Entorno virtual encontrado"
    source venv/bin/activate
    echo "🐍 Entorno virtual activado"
else
    echo "⚠️  Entorno virtual no encontrado, creando uno nuevo..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Solución 4: Reinstalar dependencias
echo "📦 Reinstalando dependencias..."
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    echo "📋 Instalando desde requirements.txt..."
    pip install -r requirements.txt
else
    echo "⚠️  requirements.txt no encontrado, instalando dependencias básicas..."
    pip install fastapi uvicorn pydantic sqlalchemy psycopg2-binary
fi

# Solución 5: Reiniciar la aplicación
echo "🔄 Reiniciando aplicación..."

# Buscar proceso de uvicorn y terminarlo
pkill -f "uvicorn main:app" 2>/dev/null || echo "No hay procesos uvicorn ejecutándose"

# Intentar reiniciar con supervisor
if command -v supervisorctl >/dev/null 2>&1; then
    echo "🔄 Reiniciando con supervisorctl..."
    sudo supervisorctl restart voltio-api 2>/dev/null || echo "Error con supervisorctl"
    sleep 5
    sudo supervisorctl status voltio-api 2>/dev/null || echo "Estado de supervisorctl no disponible"
fi

# Si supervisor no funciona, iniciar manualmente
if ! curl -f http://localhost:8000/ >/dev/null 2>&1; then
    echo "🚀 Iniciando aplicación manualmente..."
    nohup uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/voltio-api.log 2>&1 &
    echo "⏳ Esperando que la aplicación inicie..."
    sleep 10
fi

# Verificar que la aplicación funciona
echo "🧪 Probando endpoints..."
if curl -f http://localhost:8000/ >/dev/null 2>&1; then
    echo "✅ Endpoint principal funciona"
    # Mostrar respuesta
    echo "📊 Respuesta: $(curl -s http://localhost:8000/)"
else
    echo "❌ Endpoint principal no responde"
    echo "📄 Logs recientes:"
    tail -20 /tmp/voltio-api.log 2>/dev/null || echo "No hay logs disponibles"
fi

# Probar endpoints de test
for endpoint in "/test/quick" "/test/health" "/test/deployment"; do
    if curl -f "http://localhost:8000$endpoint" >/dev/null 2>&1; then
        echo "✅ Endpoint $endpoint funciona"
    else
        echo "⏳ Endpoint $endpoint no disponible"
    fi
done

echo ""
echo "🎉 Script completado!"
echo "📋 Resumen:"
echo "- Directorio: $(pwd)"
echo "- Usuario: $(whoami)"
echo "- Python: $(which python)"
echo "- Pip: $(which pip)"

if curl -f http://localhost:8000/ >/dev/null 2>&1; then
    echo "✅ API funcionando correctamente"
else
    echo "❌ API no responde - revisar logs"
fi
