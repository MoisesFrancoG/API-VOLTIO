#!/bin/bash
# Script de verificación de salud para API Voltio

echo "=== Health Check API Voltio ==="
echo "Fecha: $(date)"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar servicios
check_service() {
    local service=$1
    local name=$2
    
    if systemctl is-active --quiet $service; then
        echo -e "${name}: ${GREEN}✅ ACTIVO${NC}"
        return 0
    else
        echo -e "${name}: ${RED}❌ INACTIVO${NC}"
        return 1
    fi
}

# Verificar servicios del sistema
echo "🔧 Estado de servicios del sistema:"
check_service nginx "Nginx"
check_service supervisor "Supervisor"
check_service postgresql "PostgreSQL"

echo ""

# Verificar servicio de la aplicación
echo "🚀 Estado de la aplicación:"
if sudo supervisorctl status voltio-api | grep -q "RUNNING"; then
    echo -e "API Voltio: ${GREEN}✅ CORRIENDO${NC}"
    API_STATUS=0
else
    echo -e "API Voltio: ${RED}❌ DETENIDA${NC}"
    API_STATUS=1
fi

echo ""

# Verificar respuesta de la API
echo "🌐 Verificando respuesta de la API:"
if curl -s --max-time 10 http://localhost:8000/ > /dev/null; then
    RESPONSE=$(curl -s http://localhost:8000/ | jq -r '.message' 2>/dev/null)
    if [ "$RESPONSE" != "null" ] && [ "$RESPONSE" != "" ]; then
        echo -e "Respuesta HTTP: ${GREEN}✅ OK${NC}"
        echo "Mensaje: $RESPONSE"
    else
        echo -e "Respuesta HTTP: ${YELLOW}⚠️  RESPUESTA INVÁLIDA${NC}"
    fi
else
    echo -e "Respuesta HTTP: ${RED}❌ SIN RESPUESTA${NC}"
fi

echo ""

# Verificar uso de recursos
echo "📊 Uso de recursos:"
echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')%"
echo "RAM: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')"
echo "Disco: $(df -h / | awk 'NR==2{printf "%s", $5}')"

echo ""

# Verificar logs recientes
echo "📄 Últimos logs de la aplicación:"
if [ -f /var/log/voltio-api.log ]; then
    tail -n 5 /var/log/voltio-api.log | sed 's/^/  /'
else
    echo "  No se encontró archivo de log"
fi

echo ""

# Verificar conectividad a base de datos
echo "🗄️  Verificando conectividad a base de datos:"
if sudo -u deploy bash -c "cd /home/deploy/API-VOLTIO && source venv/bin/activate && python3 -c 'from src.core.db import engine; engine.execute(\"SELECT 1\").scalar(); print(\"✅ Conexión a PostgreSQL OK\")'" 2>/dev/null; then
    echo -e "PostgreSQL: ${GREEN}✅ CONECTADO${NC}"
else
    echo -e "PostgreSQL: ${RED}❌ ERROR DE CONEXIÓN${NC}"
fi

echo ""

# Verificar puertos
echo "🔌 Puertos en uso:"
echo "Puerto 80 (HTTP): $(sudo netstat -tlnp | grep :80 | wc -l) conexiones"
echo "Puerto 443 (HTTPS): $(sudo netstat -tlnp | grep :443 | wc -l) conexiones"
echo "Puerto 8000 (API): $(sudo netstat -tlnp | grep :8000 | wc -l) conexiones"

echo ""
echo "=== Fin Health Check ==="

# Código de salida basado en el estado general
if [ $API_STATUS -eq 0 ]; then
    exit 0
else
    exit 1
fi
