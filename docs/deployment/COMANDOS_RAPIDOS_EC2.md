# Guía Rápida de Comandos para EC2

## 🚀 Setup inicial r## 📊 Comandos de monitoreo

```bash
# Verificar estado de servicios
sudo supervisorctl status
sudo systemctl status nginx
sudo systemctl status postgresql

# Ver logs
sudo supervisorctl tail -f voltio-api
sudo tail -f /var/log/nginx/voltio-api.access.log
sudo tail -f /var/log/nginx/voltio-api.error.log

# Health check
./scripts/health-check.sh
```

## 🔄 Comandos de actualización

```bash
# Actualizar código
cd /home/deploy/API-VOLTIO
git pull origin main

# Reinstalar dependencias
source venv/bin/activate
pip install -r requirements.txt

# Reiniciar aplicación
sudo supervisorctl restart voltio-api
```

## 🐛 Solución de problemas comunespido

```bash
# 1. Conectar a EC2
ssh -i "tu-key.pem" ubuntu@tu-elastic-ip

# 2. Ejecutar setup inicial
wget -O setup-server.sh https://raw.githubusercontent.com/MoisesFrancoG/API-VOLTIO/main/scripts/setup-server.sh
chmod +x setup-server.sh
./setup-server.sh

# 3. Cambiar a usuario deploy
sudo su - deploy

# 4. Clonar repositorio
git clone https://github.com/MoisesFrancoG/API-VOLTIO.git
cd API-VOLTIO

# 5. Configurar aplicación
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## 🔧 Configuración de servicios

```bash
# Configurar Supervisor
sudo cp configs/supervisor.conf /etc/supervisor/conf.d/voltio-api.conf
sudo supervisorctl reread && sudo supervisorctl update
sudo supervisorctl start voltio-api

# Configurar Nginx
sudo cp configs/nginx.conf /etc/nginx/sites-available/voltio-api
sudo ln -s /etc/nginx/sites-available/voltio-api /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx
```

## 🔒 Configurar SSL

```bash
# Instalar certbot (si no está instalado)
sudo apt install certbot python3-certbot-nginx

# Verificar configuración de Nginx antes de SSL
sudo nginx -t

# Si hay error en gzip_proxied, actualizar configuración:
sudo cp configs/nginx.conf /etc/nginx/sites-available/voltio-api

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com

# Verificar renovación automática
sudo certbot renew --dry-run
```

## � Solución de problemas comunes

```bash
# Error de configuración Nginx
sudo nginx -t  # Verificar sintaxis
sudo cp configs/nginx.conf /etc/nginx/sites-available/voltio-api  # Reemplazar config
sudo systemctl restart nginx

# Si certbot falla por configuración Nginx
sudo nginx -t && sudo certbot --nginx -d tu-dominio.com

# Si la API no responde
sudo supervisorctl restart voltio-api
sudo supervisorctl status voltio-api

# Si hay problemas de BD
sudo -u postgres psql -c "SELECT version();"
python3 -c "from src.core.db import engine; print(engine.execute('SELECT 1').scalar())"

# Verificar puertos
sudo netstat -tlnp | grep :8000
sudo netstat -tlnp | grep :80

# Problemas con InfluxDB/Lecturas PZEM
# Si ves errores de validación Pydantic, verifica logs:
sudo supervisorctl tail -f voltio-api | grep -E "(ValidationError|deviceId)"

# Problemas con endpoints duplicados
# Verificar warnings en logs de FastAPI:
sudo supervisorctl tail -f voltio-api | grep -E "(Duplicate Operation ID|UserWarning)"

# Verificar dependencias de bcrypt
pip list | grep -E "(bcrypt|passlib)"
```

## 🧪 Ejecutar tests

```bash
# Tests básicos con pytest
python -m pytest run_all_tests.py::test_basic_import -v
python -m pytest run_all_tests.py::test_environment_setup -v

# Ejecutar todos los tests disponibles
python -m pytest run_all_tests.py -v

# Ejecutar tests específicos (si existen)
python -m pytest test_simple.py -v
python -m pytest test_lecturas_simple.py -v

# Ejecutar suite completa (modo interactivo)
python run_all_tests.py
```

## 📝 Variables de entorno importantes

```bash
# Editar configuración
nano .env

# Variables críticas:
# DB_NAME=voltio_db
# DB_USER=voltio_user
# DB_PASSWORD=tu_password_seguro
# SECRET_KEY=clave_super_secreta_32_caracteres
# ENVIRONMENT=production
# DEBUG=false
```

## 🔐 Secretos de GitHub Actions

En tu repositorio GitHub → Settings → Secrets and variables → Actions:

- `EC2_HOST`: La IP elástica de tu EC2
- `EC2_USER`: `deploy`
- `EC2_PRIVATE_KEY`: Contenido completo del archivo .pem

## ✅ Verificación final

```bash
# Probar API localmente
curl http://localhost:8000/

# Probar API externamente
curl http://tu-dominio.com/
curl https://tu-dominio.com/  # Si tienes SSL

# Verificar que todos los servicios están corriendo
./scripts/health-check.sh
```
