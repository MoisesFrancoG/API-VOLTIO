#!/bin/bash

echo "🔄 Forzando reinicio completo del servicio..."

# Detener completamente la aplicación
echo "⏹️ Deteniendo servicios..."
sudo pkill -f "uvicorn main:app" || echo "Proceso uvicorn no encontrado"
sudo supervisorctl stop voltio-api || echo "Supervisor no disponible"
sudo systemctl stop voltio-api || echo "Systemctl no disponible"

# Esperar un momento
echo "⏳ Esperando limpieza de procesos..."
sleep 5

# Verificar que no hay procesos ejecutándose
echo "🔍 Verificando procesos activos..."
ps aux | grep uvicorn | grep -v grep || echo "No hay procesos uvicorn activos"

# Activar entorno virtual y iniciar la aplicación
echo "🚀 Iniciando aplicación con nuevos endpoints..."
cd /home/ubuntu/API-VOLTIO
source venv/bin/activate

# Reiniciar usando supervisor (método preferido)
sudo supervisorctl start voltio-api || {
    echo "Supervisor no disponible, iniciando manualmente..."
    # Si supervisor no está disponible, iniciar manualmente
    nohup uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/voltio-api.log 2>&1 &
}

# Esperar a que la aplicación se inicie
echo "⏳ Esperando inicio de la aplicación..."
sleep 15

# Verificar estado
echo "🔍 Verificando estado del servicio..."
sudo supervisorctl status voltio-api || ps aux | grep uvicorn | grep -v grep

# Probar endpoints
echo "🧪 Probando endpoints..."
curl -f http://localhost:8000/ && echo " ✅ Endpoint principal OK"
curl -f http://localhost:8000/test/quick && echo " ✅ Endpoint test/quick OK" || echo " ⏳ Endpoint test/quick no disponible"
curl -f http://localhost:8000/test/health && echo " ✅ Endpoint test/health OK" || echo " ⏳ Endpoint test/health no disponible"

echo "✅ Reinicio completo finalizado"
