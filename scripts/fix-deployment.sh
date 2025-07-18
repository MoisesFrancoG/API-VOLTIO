#!/bin/bash
# Script para solucionar problemas de despliegue en EC2

echo "🔧 Solucionando problemas de despliegue..."

# Ir al directorio del proyecto
cd /home/deploy/API-VOLTIO || exit 1

echo "📁 Directorio actual: $(pwd)"

# Verificar estado de git
echo "📋 Estado de Git:"
git status

# Solución 1: Stash o commit cambios locales
echo "💾 Guardando cambios locales..."
if git diff --quiet && git diff --staged --quiet; then
    echo "✅ No hay cambios locales pendientes"
else
    echo "⚠️  Hay cambios locales. Guardándolos..."
    git stash push -m "Cambios locales antes de pull $(date)"
fi

# Solución 2: Hacer pull del código más reciente
echo "⬇️  Actualizando código desde GitHub..."
git pull origin develop

# Si hay conflictos, mostrar ayuda
if [ $? -ne 0 ]; then
    echo "❌ Error en git pull. Posibles soluciones:"
    echo "1. Revisar conflictos: git status"
    echo "2. Resetear a la versión remota: git reset --hard origin/develop"
    echo "3. O resolver manualmente los conflictos"
    echo ""
    echo "Para resetear completamente (CUIDADO - elimina cambios locales):"
    echo "git fetch origin && git reset --hard origin/develop"
    exit 1
fi

# Solución 3: Activar entorno virtual
echo "🐍 Activando entorno virtual..."
source venv/bin/activate

# Solución 4: Reinstalar dependencias limpias
echo "📦 Reinstalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Verificar que las dependencias se instalaron correctamente
if [ $? -ne 0 ]; then
    echo "❌ Error instalando dependencias. Intentando reparar..."
    
    # Crear requirements.txt limpio si está corrupto
    cat > requirements_backup.txt << 'EOF'
fastapi==0.115.14
uvicorn==0.35.0
pydantic==2.11.7
sqlalchemy==2.0.36
psycopg2-binary==2.9.10
influxdb-client==1.44.0
python-dotenv==1.0.1
passlib[bcrypt]==1.7.4
python-multipart==0.0.17
email-validator==2.2.0
python-jose[cryptography]==3.3.0
bcrypt==4.2.0
pydantic-settings==2.8.2
psutil==6.1.0
EOF
    
    echo "📋 Usando requirements de backup..."
    pip install -r requirements_backup.txt
fi

# Solución 5: Ejecutar migraciones
echo "🗄️  Ejecutando migraciones de base de datos..."
python -c "from src.core.db import engine, Base; Base.metadata.create_all(bind=engine); print('✅ Migraciones completadas')" || echo "⚠️  Error en migraciones (puede ser normal si no hay BD configurada)"

# Solución 6: Reiniciar la aplicación
echo "🔄 Reiniciando aplicación..."
sudo supervisorctl restart voltio-api

# Esperar un momento para que inicie
echo "⏳ Esperando que la aplicación inicie..."
sleep 10

# Solución 7: Verificar que la aplicación está corriendo
echo "🔍 Verificando estado de la aplicación..."
sudo supervisorctl status voltio-api

# Verificar que los endpoints responden
echo "🧪 Probando endpoints..."

# Test básico
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Endpoint / funciona"
else
    echo "❌ Endpoint / no responde"
fi

# Test de health (puede no existir en versiones anteriores)
if curl -f http://localhost:8000/test/health > /dev/null 2>&1; then
    echo "✅ Endpoint /test/health funciona"
else
    echo "⚠️  Endpoint /test/health no disponible (normal en versiones anteriores)"
fi

# Test de quick (puede no existir en versiones anteriores)
if curl -f http://localhost:8000/test/quick > /dev/null 2>&1; then
    echo "✅ Endpoint /test/quick funciona"
else
    echo "⚠️  Endpoint /test/quick no disponible (normal en versiones anteriores)"
fi

# Mostrar logs recientes
echo "📄 Últimos logs de la aplicación:"
sudo supervisorctl tail voltio-api

echo ""
echo "🎉 Script de solución completado!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Verificar que la aplicación responde: curl http://localhost:8000/"
echo "2. Ver logs en tiempo real: sudo supervisorctl tail -f voltio-api"
echo "3. Verificar estado: sudo supervisorctl status"
echo "4. Si hay problemas, revisar logs de Nginx: sudo tail -f /var/log/nginx/voltio-api.error.log"
