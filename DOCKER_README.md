# 🐋 API VOLTIO - Guía de Docker

## 📋 Archivos Creados

```
API-VOLTIO/
├── Dockerfile              # Imagen multi-stage optimizada para producción
├── .dockerignore          # Archivos excluidos de la imagen Docker
├── docker-compose.yml     # Orquestación de servicios (API + PostgreSQL + InfluxDB + RabbitMQ)
└── .env.docker            # Variables de entorno para Docker
```

---

## 🚀 Opción 1: Solo API (Dockerfile)

### Construir la imagen:

```bash
docker build -t voltio-api:latest .
```

### Ejecutar contenedor (requiere PostgreSQL e InfluxDB externos):

```bash
docker run -d \
  --name voltio-api \
  -p 8000:8000 \
  --env-file .env.docker \
  voltio-api:latest
```

### Ver logs:

```bash
docker logs -f voltio-api
```

---

## 🎯 Opción 2: Stack Completo (Docker Compose) - **RECOMENDADO**

### Levantar todos los servicios:

```bash
docker-compose up -d
```

Esto levantará:

- ✅ **PostgreSQL** en puerto `5432`
- ✅ **InfluxDB** en puerto `8086`
- ✅ **RabbitMQ** en puertos `5672` (AMQP) y `15672` (UI)
- ✅ **API FastAPI** en puerto `8000`

### Ver logs de todos los servicios:

```bash
docker-compose logs -f
```

### Ver logs solo de la API:

```bash
docker-compose logs -f api
```

### Detener servicios:

```bash
docker-compose down
```

### Detener y eliminar volúmenes (⚠️ Borra datos):

```bash
docker-compose down -v
```

---

## 🔧 Configuración

### Variables de Entorno Importantes:

**`.env.docker`** - Configuración para Docker Compose:

```env
# Base de datos (usa servicios internos de Docker)
DB_HOST=postgres          # ← Nombre del servicio Docker
INFLUX_URL=http://influxdb:8086
RABBITMQ_HOST=rabbitmq

# SSH Tunnel DESHABILITADO (no necesario en Docker)
SSH_TUNNEL_ENABLED=false
```

**`.env`** - Tu configuración local (NO se usa en Docker):

```env
DB_HOST=localhost         # ← Para desarrollo local SIN Docker
SSH_TUNNEL_ENABLED=false
```

---

## 📊 Verificar Servicios

### API:

```bash
curl http://localhost:8000/api/v1/health
```

### PostgreSQL:

```bash
docker exec -it voltio-postgres psql -U postgres -d voltio_db
```

### InfluxDB UI:

```
http://localhost:8086
Usuario: admin
Password: adminpassword
```

### RabbitMQ Management:

```
http://localhost:15672
Usuario: admin
Password: trike
```

---

## 🗄️ Ejecutar Script SQL (Crear Tablas)

### Opción A: Desde contenedor PostgreSQL

```bash
# Copiar script SQL al contenedor
docker cp tu-script.sql voltio-postgres:/tmp/

# Ejecutar dentro del contenedor
docker exec -it voltio-postgres psql -U postgres -d voltio_db -f /tmp/tu-script.sql
```

### Opción B: Desde tu máquina (requiere psql instalado)

```bash
psql -h localhost -p 5432 -U postgres -d voltio_db -f tu-script.sql
```

---

## 🔍 Troubleshooting

### Ver estado de contenedores:

```bash
docker-compose ps
```

### Reiniciar solo la API:

```bash
docker-compose restart api
```

### Reconstruir imagen después de cambios en código:

```bash
docker-compose up -d --build api
```

### Acceder a shell del contenedor API:

```bash
docker exec -it voltio-api /bin/bash
```

### Ver uso de recursos:

```bash
docker stats
```

---

## 📦 Características del Dockerfile

✅ **Multi-stage build** - Imagen final de ~200MB (sin dependencias de compilación)  
✅ **Usuario no-root** - Seguridad mejorada (usuario `voltio`)  
✅ **Health checks** - Verificación automática de disponibilidad  
✅ **Variables de entorno** - Configuración flexible sin hardcodear valores  
✅ **Cache optimizado** - Instalación rápida de dependencias

---

## 🌐 Producción

### Ejecutar con HTTPS (requiere Nginx/Traefik):

```yaml
# Agregar en docker-compose.yml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.voltio.rule=Host(`voltio.acstree.xyz`)"
  - "traefik.http.routers.voltio.tls.certresolver=letsencrypt"
```

### Variables de producción:

```env
ENVIRONMENT=production
DEBUG=false
WORKERS=4
```

---

## 🎯 Próximos Pasos

1. **Levantar stack:** `docker-compose up -d`
2. **Verificar logs:** `docker-compose logs -f api`
3. **Ejecutar script SQL** para crear tablas y SEED data
4. **Probar API:** `http://localhost:8000/docs`
