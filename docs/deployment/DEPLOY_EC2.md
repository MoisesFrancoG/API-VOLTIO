# 🚀 Guía de Despliegue en AWS EC2

## 📋 Requisitos Previos

### 1. Instancia EC2

- **Tipo recomendado:** `t3.medium` o superior (2 vCPUs, 4 GB RAM)
- **Sistema operativo:** Ubuntu 22.04 LTS
- **Almacenamiento:** Mínimo 30 GB SSD
- **Security Group:** Puertos 22 (SSH), 80 (HTTP), 443 (HTTPS)

### 2. Configurar Security Group en AWS

```
Inbound Rules:
- SSH   (22)   | TCP | Tu IP          | Administración
- HTTP  (80)   | TCP | 0.0.0.0/0      | Tráfico web
- HTTPS (443)  | TCP | 0.0.0.0/0      | Tráfico web seguro
```

---

## 🎯 Despliegue Automático

### Opción 1: Script Automatizado (Recomendado)

```bash
# 1. Conectar a EC2
ssh -i tu-llave.pem ubuntu@tu-ip-publica

# 2. Descargar y ejecutar script
curl -o deploy.sh https://raw.githubusercontent.com/MoisesFrancoG/API-VOLTIO/main/scripts/deploy-ec2.sh
chmod +x deploy.sh
./deploy.sh
```

El script automáticamente:

- ✅ Instala Docker y Docker Compose
- ✅ Clona el repositorio
- ✅ Configura SSL con Let's Encrypt
- ✅ Levanta todos los servicios
- ✅ Configura firewall

---

## 🔧 Despliegue Manual

### 1. Conectar a EC2

```bash
ssh -i voltio-key.pem ubuntu@tu-ip-ec2
```

### 2. Instalar Docker

```bash
# Actualizar sistema
sudo apt-get update && sudo apt-get upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Cerrar sesión y volver a conectar
exit
ssh -i voltio-key.pem ubuntu@tu-ip-ec2
```

### 3. Clonar Repositorio

```bash
sudo mkdir -p /opt/voltio-api
sudo chown -R $USER:$USER /opt/voltio-api
cd /opt/voltio-api
git clone https://github.com/MoisesFrancoG/API-VOLTIO.git .
```

### 4. Configurar Variables de Entorno

```bash
# Copiar template
cp .env.production .env

# Editar con credenciales reales
nano .env
```

**IMPORTANTE:** Cambiar estos valores:

```env
DB_PASSWORD=CONTRASEÑA_SEGURA_UNICA
INFLUX_TOKEN=TOKEN_ALEATORIO_MUY_LARGO
INFLUX_ADMIN_PASSWORD=CONTRASEÑA_INFLUX
RABBITMQ_PASSWORD=CONTRASEÑA_RABBITMQ
SECRET_KEY=CLAVE_JWT_SUPER_LARGA_Y_ALEATORIA
CORS_ORIGINS=https://tu-dominio.com
```

### 5. Configurar SSL (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt-get install -y certbot

# Obtener certificado
sudo certbot certonly --standalone -d voltio.acstree.xyz

# Copiar certificados
mkdir -p nginx/ssl
sudo cp /etc/letsencrypt/live/voltio.acstree.xyz/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/voltio.acstree.xyz/privkey.pem nginx/ssl/
sudo chown -R $USER:$USER nginx/ssl
```

### 6. Levantar Servicios

```bash
# Construir imágenes
docker-compose -f docker-compose.prod.yml build

# Levantar stack
docker-compose -f docker-compose.prod.yml up -d

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 7. Configurar Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 🔍 Verificación

### Comprobar servicios

```bash
# Estado de contenedores
docker-compose -f /opt/voltio-api/docker-compose.prod.yml ps

# Logs de API
docker-compose -f /opt/voltio-api/docker-compose.prod.yml logs -f api

# Health check
curl http://localhost:8000/api/v1/health
```

### Acceder a servicios

```
API Swagger:      https://voltio.acstree.xyz/docs
PostgreSQL:       localhost:5432 (solo accesible desde contenedores)
InfluxDB UI:      http://localhost:8086 (túnel SSH para acceder)
RabbitMQ UI:      http://localhost:15672 (túnel SSH para acceder)
```

---

## 🗄️ Ejecutar Script SQL

### Crear tablas y seed data

```bash
# Copiar script SQL a EC2
scp -i voltio-key.pem tu-script.sql ubuntu@tu-ip:/opt/voltio-api/

# Ejecutar en PostgreSQL
docker exec -i voltio-postgres psql -U voltio_admin -d voltio_db < /opt/voltio-api/tu-script.sql
```

---

## 🔄 Actualización de Código

```bash
cd /opt/voltio-api
git pull origin main
docker-compose -f docker-compose.prod.yml up -d --build
```

---

## 📊 Monitoreo

### Ver logs en tiempo real

```bash
# Todos los servicios
docker-compose -f docker-compose.prod.yml logs -f

# Solo API
docker-compose -f docker-compose.prod.yml logs -f api

# Solo PostgreSQL
docker-compose -f docker-compose.prod.yml logs -f postgres
```

### Estadísticas de recursos

```bash
docker stats
```

---

## 🛠️ Mantenimiento

### Backup de PostgreSQL

```bash
# Crear backup
docker exec voltio-postgres pg_dump -U voltio_admin voltio_db > backup_$(date +%Y%m%d).sql

# Restaurar backup
docker exec -i voltio-postgres psql -U voltio_admin voltio_db < backup_20250128.sql
```

### Reiniciar servicios

```bash
# Reiniciar todo
docker-compose -f docker-compose.prod.yml restart

# Reiniciar solo API
docker-compose -f docker-compose.prod.yml restart api
```

### Detener servicios

```bash
docker-compose -f docker-compose.prod.yml down
```

### Limpiar volúmenes (⚠️ BORRA DATOS)

```bash
docker-compose -f docker-compose.prod.yml down -v
```

---

## 🔐 Seguridad

### Renovar certificados SSL automáticamente

```bash
# Agregar a crontab
sudo crontab -e

# Agregar línea:
0 0 1 * * certbot renew --quiet && cp /etc/letsencrypt/live/voltio.acstree.xyz/*.pem /opt/voltio-api/nginx/ssl/ && docker-compose -f /opt/voltio-api/docker-compose.prod.yml restart nginx
```

### Acceso SSH seguro

```bash
# Deshabilitar login con password
sudo nano /etc/ssh/sshd_config
# PasswordAuthentication no
sudo systemctl restart sshd
```

---

## 🎯 Arquitectura de Producción

```
Internet (Port 443/80)
         ↓
    [Nginx Reverse Proxy]
         ↓
    [API FastAPI :8000]
    ↓     ↓     ↓
[PostgreSQL] [InfluxDB] [RabbitMQ]
    :5432      :8086      :5672
```

**Características:**

- ✅ SSL/TLS con Let's Encrypt
- ✅ Rate limiting en Nginx
- ✅ Logs con rotación automática
- ✅ Health checks en todos los servicios
- ✅ Restart automático en caso de fallo
- ✅ Red interna aislada
- ✅ Puertos de BD solo accesibles internamente

---

## 📞 Troubleshooting

### Problema: Contenedores no inician

```bash
# Ver logs detallados
docker-compose -f docker-compose.prod.yml logs

# Reconstruir sin cache
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

### Problema: Error de conexión a BD

```bash
# Verificar que PostgreSQL esté corriendo
docker-compose -f docker-compose.prod.yml ps postgres

# Probar conexión
docker exec -it voltio-postgres psql -U voltio_admin -d voltio_db
```

### Problema: Sin espacio en disco

```bash
# Limpiar imágenes no usadas
docker system prune -a --volumes
```

---

## 🎉 ¡Listo!

Tu API VOLTIO está ahora corriendo en producción en AWS EC2 con:

- ✅ HTTPS configurado
- ✅ Base de datos persistente
- ✅ Backups automáticos
- ✅ Monitoreo y logs
- ✅ Auto-restart en fallos
