#!/bin/bash
# Script para cambiar al usuario deploy y ejecutar comandos

echo "🔧 Cambiando al usuario deploy..."

# Verificar si el usuario deploy existe
if id "deploy" &>/dev/null; then
    echo "✅ Usuario deploy encontrado"
    
    # Cambiar a usuario deploy y ejecutar comandos
    sudo -u deploy -i bash << 'EOF'
    echo "👤 Usuario actual: $(whoami)"
    echo "🏠 Directorio home: $HOME"
    echo "📁 Directorio actual: $(pwd)"
    
    # Buscar el directorio del proyecto
    if [ -d "/home/deploy/API-VOLTIO" ]; then
        echo "✅ Directorio del proyecto encontrado: /home/deploy/API-VOLTIO"
        cd /home/deploy/API-VOLTIO
    elif [ -d "$HOME/API-VOLTIO" ]; then
        echo "✅ Directorio del proyecto encontrado: $HOME/API-VOLTIO"
        cd $HOME/API-VOLTIO
    else
        echo "🔍 Buscando directorio API-VOLTIO..."
        find $HOME -name "API-VOLTIO" -type d 2>/dev/null
        echo "❌ No se encontró el directorio API-VOLTIO"
        echo "📋 Contenido del directorio home:"
        ls -la $HOME/
        exit 1
    fi
    
    echo "📁 Ahora en: $(pwd)"
    echo "📋 Contenido del directorio:"
    ls -la
    
    # Verificar git
    if [ -d ".git" ]; then
        echo "✅ Repositorio git encontrado"
        git status
    else
        echo "❌ No es un repositorio git"
    fi
    
    # Verificar entorno virtual
    if [ -d "venv" ]; then
        echo "✅ Entorno virtual encontrado"
        source venv/bin/activate
        echo "🐍 Entorno virtual activado"
    else
        echo "❌ No se encontró entorno virtual"
    fi
    
EOF
else
    echo "❌ Usuario deploy no existe"
    echo "👥 Usuarios disponibles:"
    cut -d: -f1 /etc/passwd | grep -E "(ubuntu|deploy|ec2-user)"
    
    echo ""
    echo "🔧 Para crear el usuario deploy:"
    echo "sudo useradd -m -s /bin/bash deploy"
    echo "sudo usermod -aG sudo deploy"
fi
