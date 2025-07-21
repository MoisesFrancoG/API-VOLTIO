# 🧪 Endpoints de Prueba para Verificar Despliegues - v1.2.0

## 📋 Tabla de Contenidos

1. [Endpoints Disponibles](#endpoints-disponibles)
2. [Nuevos Endpoints v1.2.0](#nuevos-endpoints-v120)
3. [Cómo usar los endpoints](#cómo-usar-los-endpoints)
4. [Ejemplos de respuestas](#ejemplos-de-respuestas)
5. [Verificación de despliegues](#verificación-de-despliegues)

---

## 🎯 Endpoints Disponibles

### Endpoints Básicos (v1.0)

### 1. **GET `/test/quick`** - Verificación Rápida

- **Propósito**: Endpoint ultra simple para verificaciones rápidas
- **Uso**: Comprobar que la API responde básicamente
- **Tiempo de respuesta**: < 50ms

### 2. **GET `/test/health`** - Health Check

- **Propósito**: Health check estándar para monitoreo
- **Uso**: Verificar el estado de salud de la aplicación
- **Ideal para**: Load balancers, monitoreo automático

### 3. **GET `/test/deployment`** - Información Completa de Despliegue

- **Propósito**: Información detallada sobre el estado del despliegue
- **Uso**: Verificar que todos los módulos y configuraciones están funcionando
- **Incluye**: Versión, módulos, configuración, sistema

---

## 🆕 Nuevos Endpoints v1.2.0

### 4. **GET `/test/deployment-v2`** - Despliegue v2 (NUEVO)

- **Propósito**: Validar los últimos cambios y configuración del usuario deploy
- **Uso**: Verificar que el nuevo sistema de despliegue funciona correctamente
- **Incluye**:
  - Contexto del usuario (deploy/ubuntu)
  - Información de Git
  - Características del nuevo despliegue
  - Directorio de trabajo actual

### 5. **GET `/test/system-info`** - Información Detallada del Sistema (NUEVO)

- **Propósito**: Diagnosticar la configuración del servidor en detalle
- **Uso**: Obtener información completa del entorno de ejecución
- **Incluye**:
  - Información del servidor (hostname, platform)
  - Proceso actual (PID, memoria, CPU)
  - Directorios y archivos importantes
  - Estado del entorno virtual
  - Información de red

### 6. **GET `/test/database-check`** - Verificación de Bases de Datos (NUEVO)

- **Propósito**: Comprobar conectividad con PostgreSQL e InfluxDB
- **Uso**: Validar que las conexiones a BD funcionan
- **Incluye**:
  - Estado de conexión PostgreSQL
  - Estado de conexión InfluxDB
  - Versiones de las bases de datos
  - Mensajes de error detallados

### 7. **GET `/test/environment-vars`** - Variables de Entorno (NUEVO)

- **Propósito**: Verificar configuración sin exponer secretos
- **Uso**: Comprobar que todas las variables críticas están configuradas
- **Incluye**:
  - Estado de variables críticas
  - Longitud de valores (sin mostrar contenido)
  - Resumen de configuración
  - Variables faltantes

### 8. **GET `/test/api-performance`** - Test de Rendimiento (NUEVO)

- **Propósito**: Medir rendimiento básico de la API
- **Uso**: Verificar que el servidor responde con buen rendimiento
- **Incluye**:
  - Tiempo de procesamiento
  - Items procesados por segundo
  - Carga del servidor (CPU, memoria)
  - Estado de rendimiento

### 9. **GET `/test/all-endpoints`** - Resumen de Todos los Tests (NUEVO)

- **Propósito**: Listar todos los endpoints de prueba disponibles
- **Uso**: Obtener una vista general de todas las pruebas
- **Incluye**:
  - Lista completa de endpoints
  - Descripción de cada uno
  - Resumen de características
  - Instrucciones de uso

### 4. **GET `/`** - Endpoint Principal

- **Propósito**: Endpoint raíz de la API
- **Uso**: Verificación básica de que la API está corriendo

---

## 🚀 Cómo usar los endpoints

### En desarrollo local:

```bash
# Iniciar la API
uvicorn main:app --host 0.0.0.0 --port 8000

# Probar endpoints
curl http://localhost:8000/test/quick
curl http://localhost:8000/test/health
curl http://localhost:8000/test/deployment
```

### En producción:

```bash
# Reemplaza 'tu-dominio.com' con tu dominio o IP
curl https://tu-dominio.com/test/quick
curl https://tu-dominio.com/test/health
curl https://tu-dominio.com/test/deployment

# O con IP directa
curl http://tu-ip-ec2:8000/test/quick
```

### Desde navegador:

- `https://tu-dominio.com/test/quick`
- `https://tu-dominio.com/test/health`
- `https://tu-dominio.com/test/deployment`

---

## 📄 Ejemplos de respuestas

### `/test/quick`

```json
{
  "ok": true,
  "time": "2025-07-17T23:45:42.175637",
  "message": "🚀 Despliegue exitoso - API respondiendo correctamente"
}
```

### `/test/health`

```json
{
  "status": "healthy",
  "timestamp": "2025-07-17T23:45:42.175637",
  "uptime": "running",
  "version": "1.1.0",
  "service": "API Voltio"
}
```

### `/test/deployment` (resumido)

```json
{
  "status": "✅ API funcionando correctamente",
  "message": "Este endpoint confirma que el despliegue fue exitoso",
  "timestamp": "2025-07-17T23:45:42.175637",
  "version": "1.1.0",
  "environment": "production",
  "deployment": {
    "date": "2025-07-17 23:45:42",
    "features": [
      "🧪 Tests corregidos y funcionando",
      "📁 Estructura de proyecto validada",
      "🚀 GitHub Actions configurado"
    ]
  },
  "modules_status": {
    "usuarios": "✅ Disponible",
    "roles": "✅ Disponible",
    "ubicaciones": "✅ Disponible"
  }
}
```

---

## ✅ Verificación de despliegues

### 1. **Verificación inmediata después del despliegue:**

```bash
# Verificar que responde
curl -f https://tu-dominio.com/test/quick

# Si responde con {"ok": true, ...} el despliegue fue exitoso
```

### 2. **Verificación detallada:**

```bash
# Obtener información completa
curl https://tu-dominio.com/test/deployment | jq '.'

# Verificar versión específica
curl https://tu-dominio.com/test/deployment | jq '.version'

# Verificar que todos los módulos están disponibles
curl https://tu-dominio.com/test/deployment | jq '.modules_status'
```

### 3. **Script de verificación automática:**

```bash
#!/bin/bash
# verify-deployment.sh

DOMAIN="tu-dominio.com"
echo "🔍 Verificando despliegue en $DOMAIN..."

# Test básico
if curl -f https://$DOMAIN/test/quick > /dev/null 2>&1; then
    echo "✅ API responde correctamente"
else
    echo "❌ API no responde"
    exit 1
fi

# Obtener versión
VERSION=$(curl -s https://$DOMAIN/test/health | jq -r '.version')
echo "📦 Versión desplegada: $VERSION"

# Verificar timestamp
TIMESTAMP=$(curl -s https://$DOMAIN/test/quick | jq -r '.time')
echo "⏰ Última respuesta: $TIMESTAMP"

echo "🎉 Verificación completada exitosamente!"
```

### 4. **Monitoreo continuo:**

```bash
# Verificar cada 30 segundos
watch -n 30 'curl -s https://tu-dominio.com/test/health | jq ".status"'

# O con fecha/hora
watch -n 30 'echo "$(date): $(curl -s https://tu-dominio.com/test/quick | jq -r ".message")"'
```

---

## 🔧 Integración con GitHub Actions

Los endpoints se prueban automáticamente en el workflow de GitHub Actions:

```yaml
# En .github/workflows/deploy.yml
- name: Verify deployment
  run: |
    # Verificar que la API responda
    curl -f http://localhost:8000/ || exit 1

    # Probar endpoints de test
    curl -f http://localhost:8000/test/quick || exit 1
    curl -f http://localhost:8000/test/health || exit 1
```

---

## 📊 Monitoreo en producción

### Con herramientas de monitoreo:

**Uptime Robot / Pingdom:**

- URL: `https://tu-dominio.com/test/health`
- Intervalo: 5 minutos
- Palabra clave esperada: `"healthy"`

**New Relic / DataDog:**

- Endpoint: `/test/health`
- Métrica: Tiempo de respuesta
- Alerta: Si status != "healthy"

**Prometheus + Grafana:**

```yaml
# prometheus.yml
- job_name: "voltio-api"
  static_configs:
    - targets: ["tu-dominio.com:443"]
  metrics_path: "/test/health"
```

---

## 🚨 Troubleshooting

### Si los endpoints no responden:

1. **Verificar que la aplicación está corriendo:**

   ```bash
   sudo supervisorctl status voltio-api
   ```

2. **Verificar logs:**

   ```bash
   sudo supervisorctl tail -f voltio-api
   ```

3. **Verificar puerto:**

   ```bash
   sudo netstat -tlnp | grep :8000
   ```

4. **Probar localmente:**
   ```bash
   curl http://localhost:8000/test/quick
   ```

### Códigos de respuesta esperados:

- ✅ **200**: Todo funcionando correctamente
- ❌ **500**: Error interno del servidor
- ❌ **404**: Endpoint no encontrado (verificar despliegue)
- ❌ **Connection refused**: Aplicación no está corriendo

---

**¡Con estos endpoints puedes verificar rápidamente que tus despliegues fueron exitosos! 🚀**
