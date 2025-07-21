# Guía Completa: Despliegue de API Voltio en EC2 con GitHub Actions

## 📋 Tabla de Contenidos

1. [Configuración inicial de EC2](#configuración-inicial-de-ec2)
2. [Preparación del servidor Ubuntu](#preparación-del-servidor-ubuntu)
3. [Configuración de la base de datos](#configuración-de-la-base-de-datos)
4. [Despliegue manual inicial](#despliegue-manual-inicial)
5. [Configuración de GitHub Actions](#configuración-de-github-actions)
6. [Variables de entorno y secretos](#variables-de-entorno-y-secretos)
7. [Monitoreo y mantenimiento](#monitoreo-y-mantenimiento)

---

## 🚀 Configuración inicial de EC2

### 1. Crear instancia EC2

1. **Inicia sesión en AWS Console**
2. **Ir a EC2 Dashboard**
3. **Launch Instance** con la siguiente configuración:
   - **OS**: Ubuntu Server 22.04 LTS (64-bit)
   - **Instance Type**: t3.medium (mínimo recomendado)
   - **Key Pair**: Crear o usar existente para SSH
   - **Security Group**: Configurar puertos:
     - `22` (SSH)
     - `80` (HTTP)
     - `443` (HTTPS)
     - `8000` (API - temporal para pruebas)
   - **Storage**: 20 GB mínimo

### 2. Configurar Elastic IP (Recomendado)

```bash
# En AWS Console, ir a EC2 > Elastic IPs
# Allocate new address y asociar con la instancia
```

### 3. Configurar dominio (opcional)

- Configura un registro A en tu DNS apuntando a la Elastic IP
- Ejemplo: `api.tudominio.com` → `tu-elastic-ip`

---

## 🛠️ Preparación del servidor Ubuntu

### 1. Conectar via SSH

```bash
# Desde tu máquina local
ssh -i "tu-key.pem" ubuntu@tu-elastic-ip
```

### 2. Actualizar sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Instalar dependencias del sistema

```bash
# Python y herramientas de desarrollo
sudo apt install -y python3 python3-pip python3-venv git curl software-properties-common

# PostgreSQL (opcional, si vas a usar BD local)
sudo apt install -y postgresql postgresql-contrib

# Nginx (servidor web)
sudo apt install -y nginx

# Supervisord (gestor de procesos)
sudo apt install -y supervisor

# Herramientas de sistema
sudo apt install -y htop tree unzip
```

### 4. Configurar usuario deploy (recomendado)

```bash
# Crear usuario para despliegues
sudo adduser deploy
sudo usermod -aG sudo deploy

# Configurar SSH para el usuario deploy
sudo mkdir -p /home/deploy/.ssh
sudo cp ~/.ssh/authorized_keys /home/deploy/.ssh/
sudo chown -R deploy:deploy /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh
sudo chmod 600 /home/deploy/.ssh/authorized_keys
```

---

## 🗄️ Configuración de la base de datos

### Opción A: PostgreSQL local

```bash
# Configurar PostgreSQL
sudo -u postgres createuser --interactive
# Nombre: voltio_user
# ¿Superuser? No
# ¿Crear bases de datos? Sí
# ¿Crear roles? No

# Crear base de datos
sudo -u postgres createdb voltio_db -O voltio_user

# Configurar contraseña
sudo -u postgres psql
postgres=# ALTER USER voltio_user PASSWORD 'tu_password_seguro';
postgres=# \q
```

### Opción B: Base de datos externa (RDS, etc.)

- Configurar RDS PostgreSQL en AWS
- Anotar: host, port, database, username, password

---

## 📦 Despliegue manual inicial

### 1. Clonar repositorio

```bash
# Cambiar a usuario deploy
sudo su - deploy

# Clonar repositorio
git clone https://github.com/MoisesFrancoG/API-VOLTIO.git
cd API-VOLTIO
```

### 2. Configurar entorno Python

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
# Crear archivo .env
cp .env.example .env  # Si existe
# O crear manualmente:
nano .env
```

**Contenido del archivo `.env`:**

```env
# Base de datos PostgreSQL
DB_NAME=voltio_db
DB_USER=voltio_user
DB_PASSWORD=tu_password_seguro
DB_HOST=localhost
DB_PORT=5432

# InfluxDB
INFLUX_URL=https://tu-influx-url:8086
INFLUX_TOKEN=tu_influx_token
INFLUX_ORG=tu_organizacion
INFLUX_BUCKET=voltio_readings

# Seguridad
SECRET_KEY=tu_secret_key_muy_seguro_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# SSH Tunnel (si aplica)
SSH_TUNNEL_ENABLED=false
SSH_HOST=tu_ssh_host
SSH_PORT=22
SSH_USER=tu_ssh_user
SSH_KEY_PATH=/path/to/key
LOCAL_PORT=5432
REMOTE_HOST=localhost
REMOTE_PORT=5432

# Configuración de producción
ENVIRONMENT=production
DEBUG=false
```

### 4. Probar la aplicación

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar migraciones (si aplica)
python -c "from src.core.db import engine, Base; Base.metadata.create_all(bind=engine)"

# Probar la API
uvicorn main:app --host 0.0.0.0 --port 8000

# En otra terminal, probar:
curl http://localhost:8000/
```

### 5. Configurar Supervisor

```bash
# Crear configuración de supervisor
sudo nano /etc/supervisor/conf.d/voltio-api.conf
```

**Contenido del archivo supervisor:**

```ini
[program:voltio-api]
command=/home/deploy/API-VOLTIO/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
directory=/home/deploy/API-VOLTIO
user=deploy
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/voltio-api.log
environment=PATH="/home/deploy/API-VOLTIO/venv/bin"
```

```bash
# Recargar supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start voltio-api

# Verificar estado
sudo supervisorctl status
```

### 6. Configurar Nginx

```bash
# Crear configuración de Nginx
sudo nano /etc/nginx/sites-available/voltio-api
```

**Contenido de Nginx:**

```nginx
server {
    listen 80;
    server_name tu-dominio.com tu-elastic-ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Logs
    access_log /var/log/nginx/voltio-api.access.log;
    error_log /var/log/nginx/voltio-api.error.log;
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/voltio-api /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Probar configuración
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

### 7. Configurar SSL con Let's Encrypt

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com

# Verificar renovación automática
sudo certbot renew --dry-run
```

---

## ⚙️ Configuración de GitHub Actions

### 1. Crear directorio de workflows

```bash
# En tu repositorio local
mkdir -p .github/workflows
```

### 2. Crear archivo de workflow

Crear `.github/workflows/deploy.yml`:

```yaml
name: Deploy to EC2

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_USER: testuser
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-asyncio httpx

      - name: Create test .env file
        run: |
          echo "DB_NAME=testdb" >> .env
          echo "DB_USER=testuser" >> .env
          echo "DB_PASSWORD=testpass" >> .env
          echo "DB_HOST=localhost" >> .env
          echo "DB_PORT=5432" >> .env
          echo "INFLUX_URL=http://localhost:8086" >> .env
          echo "INFLUX_TOKEN=test-token" >> .env
          echo "INFLUX_ORG=test-org" >> .env
          echo "INFLUX_BUCKET=test-bucket" >> .env
          echo "SECRET_KEY=test-secret-key" >> .env
          echo "SSH_TUNNEL_ENABLED=false" >> .env

      - name: Run tests
        run: |
          python -m pytest run_all_tests.py -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop'

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to EC2
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USER }}
          key: ${{ secrets.EC2_PRIVATE_KEY }}
          script: |
            cd /home/deploy/API-VOLTIO
            git pull origin ${{ github.ref_name }}
            source venv/bin/activate
            pip install -r requirements.txt

            # Ejecutar migraciones si es necesario
            python -c "from src.core.db import engine, Base; Base.metadata.create_all(bind=engine)"

            # Reiniciar la aplicación
            sudo supervisorctl restart voltio-api

            # Verificar que el servicio esté corriendo
            sleep 5
            sudo supervisorctl status voltio-api

            # Verificar que la API responda
            curl -f http://localhost:8000/ || exit 1
```

---

## 🔐 Variables de entorno y secretos

### 1. En GitHub (Settings > Secrets and variables > Actions)

**Secrets necesarios:**

- `EC2_HOST`: IP elástica de tu instancia EC2
- `EC2_USER`: `deploy` (o usuario que configuraste)
- `EC2_PRIVATE_KEY`: Contenido completo de tu archivo `.pem`

**Variables de entorno (si necesario):**

- `ENVIRONMENT`: `production`

### 2. Crear script de configuración de secretos

Crear `scripts/setup-secrets.sh`:

```bash
#!/bin/bash
# Script para configurar secretos de producción

# Verificar que estamos en el servidor correcto
if [ ! -f "/home/deploy/API-VOLTIO/.env" ]; then
    echo "Error: No estás en el servidor de producción"
    exit 1
fi

# Backup del .env actual
cp /home/deploy/API-VOLTIO/.env /home/deploy/API-VOLTIO/.env.backup.$(date +%Y%m%d_%H%M%S)

# Generar SECRET_KEY seguro
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

echo "SECRET_KEY generado: $SECRET_KEY"
echo "Actualiza tu archivo .env con esta clave"
```

---

## 📊 Monitoreo y mantenimiento

### 1. Scripts de monitoreo

Crear `scripts/health-check.sh`:

```bash
#!/bin/bash
# Script de verificación de salud

echo "=== Health Check API Voltio ==="
echo "Fecha: $(date)"

# Verificar servicio supervisor
echo "Estado Supervisor:"
sudo supervisorctl status voltio-api

# Verificar Nginx
echo "Estado Nginx:"
sudo systemctl status nginx --no-pager -l

# Verificar respuesta de la API
echo "Respuesta de la API:"
curl -s http://localhost:8000/ | jq '.' || echo "Error en respuesta JSON"

# Verificar logs recientes
echo "Últimos logs de la aplicación:"
tail -n 10 /var/log/voltio-api.log

echo "=== Fin Health Check ==="
```

### 2. Configurar monitoreo automático

```bash
# Agregar al crontab
crontab -e

# Verificar cada 5 minutos
*/5 * * * * /home/deploy/scripts/health-check.sh > /var/log/health-check.log 2>&1
```

### 3. Logs importantes

```bash
# Logs de la aplicación
tail -f /var/log/voltio-api.log

# Logs de Nginx
tail -f /var/log/nginx/voltio-api.access.log
tail -f /var/log/nginx/voltio-api.error.log

# Logs del sistema
sudo journalctl -u nginx -f
sudo journalctl -u supervisor -f
```

---

## 🔧 Comandos útiles

### Gestión de la aplicación

```bash
# Reiniciar aplicación
sudo supervisorctl restart voltio-api

# Ver logs en tiempo real
sudo supervisorctl tail -f voltio-api

# Reiniciar Nginx
sudo systemctl restart nginx

# Verificar puertos
sudo netstat -tlnp | grep :8000
sudo netstat -tlnp | grep :80
```

### Actualización manual

```bash
cd /home/deploy/API-VOLTIO
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart voltio-api
```

### Backup de base de datos

```bash
# PostgreSQL
pg_dump -h localhost -U voltio_user voltio_db > backup_$(date +%Y%m%d).sql

# Restaurar
psql -h localhost -U voltio_user voltio_db < backup_20240101.sql
```

---

## 🚨 Solución de problemas comunes

### 1. API no responde

```bash
# Verificar proceso
sudo supervisorctl status voltio-api

# Revisar logs
tail -50 /var/log/voltio-api.log

# Reiniciar
sudo supervisorctl restart voltio-api
```

### 2. Error de base de datos

```bash
# Verificar conexión a BD
python3 -c "from src.core.db import engine; print(engine.execute('SELECT 1').scalar())"

# Verificar variables de entorno
python3 -c "from src.core.config import settings; print('Config loaded successfully')"
```

### 3. Error de SSL

```bash
# Renovar certificado
sudo certbot renew

# Verificar configuración Nginx
sudo nginx -t
```

---

## ✅ Checklist de despliegue

### Configuración inicial

- [ ] Instancia EC2 configurada
- [ ] Elastic IP asignada
- [ ] Security Groups configurados
- [ ] Usuario deploy creado
- [ ] Dependencias del sistema instaladas

### Base de datos

- [ ] PostgreSQL configurado (local o RDS)
- [ ] InfluxDB configurado
- [ ] Variables de entorno configuradas
- [ ] Conexiones probadas

### Aplicación

- [ ] Repositorio clonado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Archivo .env configurado
- [ ] API funcionando en puerto 8000

### Servicios del sistema

- [ ] Supervisor configurado
- [ ] Nginx configurado
- [ ] SSL configurado (opcional)
- [ ] Firewall configurado

### GitHub Actions

- [ ] Workflow creado
- [ ] Secrets configurados en GitHub
- [ ] Deploy automático probado

### Monitoreo

- [ ] Scripts de health check
- [ ] Logs configurados
- [ ] Monitoreo automático (opcional)

---

## 📞 Soporte

Si encuentras problemas durante el despliegue:

1. **Revisar logs**: Siempre empezar por los logs de la aplicación y del sistema
2. **Verificar conectividad**: Probar conexiones a bases de datos y servicios externos
3. **Probar manualmente**: Ejecutar comandos paso a paso para identificar el problema
4. **Consultar documentación**: FastAPI, Nginx, Supervisor, AWS EC2

**¡Tu API Voltio estará lista para producción! 🚀**
