#!/bin/bash

# ==============================================================================
# SCRIPT DE CONFIGURACIÓN SSL CON CERTBOT
# Ejecutar DESPUÉS de levantar docker-compose.ssl.yml
# ==============================================================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔐 Configuración de SSL para API VOLTIO${NC}"
echo ""

# ------------------------------------------------------------------------------
# 1. Solicitar información
# ------------------------------------------------------------------------------
read -p "Ingresa tu dominio (ej: voltioapi.tudominio.com): " DOMAIN
read -p "Ingresa tu email para notificaciones SSL: " EMAIL

# ------------------------------------------------------------------------------
# 2. Verificar que Nginx esté corriendo
# ------------------------------------------------------------------------------
echo -e "${YELLOW}📋 Verificando que Nginx esté corriendo...${NC}"
if ! docker ps | grep -q voltio-nginx; then
    echo -e "${RED}❌ Nginx no está corriendo. Ejecuta primero:${NC}"
    echo "   docker-compose -f docker-compose.ssl.yml up -d"
    exit 1
fi

echo -e "${GREEN}✅ Nginx está corriendo${NC}"

# ------------------------------------------------------------------------------
# 3. Obtener certificado SSL
# ------------------------------------------------------------------------------
echo -e "${YELLOW}🔒 Obteniendo certificado SSL de Let's Encrypt...${NC}"

docker run --rm \
    -v certbot_certs:/etc/letsencrypt \
    -v certbot_webroot:/var/www/certbot \
    certbot/certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Certificado obtenido exitosamente${NC}"
else
    echo -e "${RED}❌ Error obteniendo certificado${NC}"
    exit 1
fi

# ------------------------------------------------------------------------------
# 4. Copiar certificados a carpeta nginx
# ------------------------------------------------------------------------------
echo -e "${YELLOW}📁 Copiando certificados...${NC}"

docker run --rm \
    -v certbot_certs:/etc/letsencrypt \
    -v $(pwd)/nginx/ssl:/nginx/ssl \
    alpine sh -c "cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem /nginx/ssl/ && \
                  cp /etc/letsencrypt/live/$DOMAIN/privkey.pem /nginx/ssl/ && \
                  chmod 644 /nginx/ssl/*.pem"

echo -e "${GREEN}✅ Certificados copiados${NC}"

# ------------------------------------------------------------------------------
# 5. Reiniciar Nginx para aplicar certificados
# ------------------------------------------------------------------------------
echo -e "${YELLOW}🔄 Reiniciando Nginx...${NC}"
docker-compose -f docker-compose.ssl.yml restart nginx

echo -e "${GREEN}✅ Nginx reiniciado${NC}"

# ------------------------------------------------------------------------------
# 6. Verificar SSL
# ------------------------------------------------------------------------------
echo ""
echo -e "${GREEN}🎉 ¡Configuración SSL completada!${NC}"
echo ""
echo -e "${YELLOW}🌐 Tu API está disponible en:${NC}"
echo "   https://$DOMAIN/docs"
echo ""
echo -e "${YELLOW}🔍 Verifica SSL en:${NC}"
echo "   https://www.ssllabs.com/ssltest/analyze.html?d=$DOMAIN"
echo ""
echo -e "${YELLOW}♻️  Renovación automática:${NC}"
echo "   Los certificados se renovarán automáticamente cada 12 horas"
echo ""
