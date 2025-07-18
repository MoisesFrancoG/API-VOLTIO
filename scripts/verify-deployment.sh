#!/bin/bash
# Script para verificar el estado de despliegue en producción

DOMAIN="voltioapi.acstree.xyz"
echo "🔍 Verificando estado de despliegue en $DOMAIN..."
echo "=================================================="

# Función para hacer requests con manejo de errores
check_endpoint() {
    local endpoint=$1
    local description=$2
    
    echo ""
    echo "🧪 Probando $description ($endpoint):"
    
    # Verificar si responde
    if curl -s --max-time 10 https://$DOMAIN$endpoint > /dev/null 2>&1; then
        echo "✅ Endpoint responde"
        
        # Obtener respuesta
        response=$(curl -s https://$DOMAIN$endpoint)
        echo "📄 Respuesta:"
        echo "$response" | jq '.' 2>/dev/null || echo "$response"
    else
        echo "❌ Endpoint no responde o no existe aún"
        echo "ℹ️  Esto es normal si el despliegue aún no incluye estos endpoints"
    fi
}

# Verificar endpoint principal
check_endpoint "/" "Endpoint principal"

# Verificar endpoints de prueba
check_endpoint "/test/quick" "Verificación rápida"
check_endpoint "/test/health" "Health check"
check_endpoint "/test/deployment" "Información de despliegue"

echo ""
echo "=================================================="
echo "📊 Resumen de verificación:"

# Verificar versión actual
echo "🔢 Intentando obtener versión..."
version=$(curl -s https://$DOMAIN/test/health 2>/dev/null | jq -r '.version' 2>/dev/null)
if [ "$version" != "null" ] && [ "$version" != "" ]; then
    echo "📦 Versión desplegada: $version"
else
    echo "⚠️  No se pudo obtener la versión (endpoints de test no disponibles)"
fi

# Verificar timestamp de última respuesta
echo "⏰ Timestamp de verificación: $(date)"

echo ""
echo "🌐 URLs para verificar manualmente:"
echo "- https://$DOMAIN/"
echo "- https://$DOMAIN/test/quick"
echo "- https://$DOMAIN/test/health"
echo "- https://$DOMAIN/test/deployment"
