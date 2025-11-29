#!/bin/bash

# ==============================================================================
# SCRIPT DE DESPLIEGUE EN AWS EC2 - API VOLTIO
# ==============================================================================

set -e  # Detener en caso de error

echo "🚀 Iniciando despliegue de API VOLTIO en EC2..."

# ------------------------------------------------------------------------------
# 1. Actualizar sistema
# ------------------------------------------------------------------------------
echo "📦 Actualizando sistema..."
sudo apt-get update
sudo apt-get upgrade -y

# ------------------------------------------------------------------------------
# 2. Instalar Docker y Docker Compose
# ------------------------------------------------------------------------------
echo "🐋 Instalando Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
else
    echo "✅ Docker ya está instalado"
fi

echo "🐋 Instalando Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
else
    echo "✅ Docker Compose ya está instalado"
fi

# ------------------------------------------------------------------------------
# 3. Crear directorio de aplicación
# ------------------------------------------------------------------------------
echo "📁 Creando estructura de directorios..."
sudo mkdir -p /opt/voltio-api
sudo chown -R $USER:$USER /opt/voltio-api
cd /opt/voltio-api

# ------------------------------------------------------------------------------
# 4. Clonar o actualizar repositorio
# ------------------------------------------------------------------------------
echo "📥 Clonando repositorio..."
if [ ! -d ".git" ]; then
    git clone https://github.com/MoisesFrancoG/API-VOLTIO.git .
else
    git pull origin main
fi

# ------------------------------------------------------------------------------
# 5. Configurar variables de entorno
# ------------------------------------------------------------------------------
echo "🔐 Configurando variables de entorno..."
if [ ! -f ".env" ]; then
    cp .env.production .env
    echo "⚠️  IMPORTANTE: Edita el archivo .env con tus credenciales reales"
    echo "⚠️  Ejecuta: nano /opt/voltio-api/.env"
    read -p "Presiona ENTER cuando hayas configurado el .env..."
fi

# ------------------------------------------------------------------------------
# 6. Crear directorios necesarios
# ------------------------------------------------------------------------------
echo "📂 Creando directorios auxiliares..."
mkdir -p backups nginx/ssl logs

# ------------------------------------------------------------------------------
# 7. Configurar SSL con Let's Encrypt (opcional)
# ------------------------------------------------------------------------------
read -p "¿Deseas configurar SSL con Let's Encrypt? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔒 Instalando Certbot..."
    sudo apt-get install -y certbot
    
    read -p "Ingresa tu dominio (ej: voltio.acstree.xyz): " DOMAIN
    
    sudo certbot certonly --standalone -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
    
    # Copiar certificados a la carpeta nginx
    sudo cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem nginx/ssl/
    sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem nginx/ssl/
    sudo chown -R $USER:$USER nginx/ssl
fi

# ------------------------------------------------------------------------------
# 8. Construir e iniciar contenedores
# ------------------------------------------------------------------------------
echo "🏗️  Construyendo imágenes Docker..."
docker-compose -f docker-compose.prod.yml build --no-cache

echo "🚀 Levantando servicios..."
docker-compose -f docker-compose.prod.yml up -d

# ------------------------------------------------------------------------------
# 9. Verificar estado
# ------------------------------------------------------------------------------
echo "⏳ Esperando que los servicios estén listos..."
sleep 15

echo "📊 Estado de los contenedores:"
docker-compose -f docker-compose.prod.yml ps

echo "📋 Logs de la API:"
docker-compose -f docker-compose.prod.yml logs --tail=50 api

# ------------------------------------------------------------------------------
# 10. Configurar firewall (UFW)
# ------------------------------------------------------------------------------
echo "🔥 Configurando firewall..."
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw --force enable

# ------------------------------------------------------------------------------
# 11. Configurar auto-renovación SSL
# ------------------------------------------------------------------------------
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "♻️  Configurando renovación automática de SSL..."
    (sudo crontab -l 2>/dev/null; echo "0 0 1 * * certbot renew --quiet && cp /etc/letsencrypt/live/$DOMAIN/*.pem /opt/voltio-api/nginx/ssl/ && docker-compose -f /opt/voltio-api/docker-compose.prod.yml restart nginx") | sudo crontab -
fi

# ------------------------------------------------------------------------------
# ✅ Finalizado
# ------------------------------------------------------------------------------
echo ""
echo "✅ ¡Despliegue completado exitosamente!"
echo ""
echo "🌐 Tu API está disponible en:"
echo "   - HTTP:  http://$(curl -s ifconfig.me)"
echo "   - HTTPS: https://$DOMAIN (si configuraste SSL)"
echo ""
echo "📊 Comandos útiles:"
echo "   - Ver logs:      docker-compose -f /opt/voltio-api/docker-compose.prod.yml logs -f"
echo "   - Reiniciar:     docker-compose -f /opt/voltio-api/docker-compose.prod.yml restart"
echo "   - Detener:       docker-compose -f /opt/voltio-api/docker-compose.prod.yml down"
echo "   - Actualizar:    cd /opt/voltio-api && git pull && docker-compose -f docker-compose.prod.yml up -d --build"
echo ""
