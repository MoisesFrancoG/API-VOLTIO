#!/bin/bash
# Script de configuración inicial para EC2 Ubuntu

echo "🚀 Iniciando configuración de servidor para API Voltio..."

# Verificar que estamos corriendo como usuario con privilegios sudo
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  No ejecutes este script como root. Usa un usuario con sudo."
    exit 1
fi

# Actualizar sistema
echo "📦 Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
echo "🔧 Instalando dependencias del sistema..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    software-properties-common \
    postgresql \
    postgresql-contrib \
    nginx \
    supervisor \
    htop \
    tree \
    unzip \
    certbot \
    python3-certbot-nginx

# Crear usuario deploy si no existe
if ! id "deploy" &>/dev/null; then
    echo "👤 Creando usuario deploy..."
    sudo adduser --disabled-password --gecos "" deploy
    sudo usermod -aG sudo deploy
    
    # Configurar SSH para usuario deploy
    sudo mkdir -p /home/deploy/.ssh
    sudo cp ~/.ssh/authorized_keys /home/deploy/.ssh/
    sudo chown -R deploy:deploy /home/deploy/.ssh
    sudo chmod 700 /home/deploy/.ssh
    sudo chmod 600 /home/deploy/.ssh/authorized_keys
    
    echo "✅ Usuario deploy creado y configurado"
else
    echo "✅ Usuario deploy ya existe"
fi

# Configurar PostgreSQL
echo "🗄️  Configurando PostgreSQL..."
sudo -u postgres psql -c "CREATE USER voltio_user WITH PASSWORD 'changeme123';" 2>/dev/null || echo "Usuario ya existe"
sudo -u postgres psql -c "CREATE DATABASE voltio_db OWNER voltio_user;" 2>/dev/null || echo "Base de datos ya existe"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE voltio_db TO voltio_user;" 2>/dev/null

# Configurar firewall
echo "🔒 Configurando firewall..."
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

echo "✅ Configuración inicial completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Cambiar a usuario deploy: sudo su - deploy"
echo "2. Clonar repositorio: git clone https://github.com/MoisesFrancoG/API-VOLTIO.git"
echo "3. Configurar la aplicación siguiendo la guía"
echo ""
echo "⚠️  IMPORTANTE: Cambiar la contraseña de PostgreSQL!"
echo "   sudo -u postgres psql -c \"ALTER USER voltio_user PASSWORD 'tu_password_seguro';\""
