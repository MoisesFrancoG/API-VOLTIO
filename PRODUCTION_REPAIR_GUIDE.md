# 🚨 DIAGNÓSTICO Y REPARACIÓN - API VOLTIO PRODUCCIÓN

## 📊 **Estado Actual:**

- ✅ **API Principal:** Funcionando (FastAPI se ejecuta)
- ✅ **Documentación:** Accesible en https://voltioapi.acstree.xyz/docs
- ❌ **Autenticación:** Error 500 en todos los endpoints de login
- ❌ **Base de Datos:** Problemas de conexión

## 🔍 **Diagnóstico Realizado:**

```
✅ Root endpoint: 200
✅ OpenAPI schema: 200
✅ Documentation: 200
❌ Users login: 500 (Internal Server Error)
❌ Todas las credenciales: 500
```

## 🛠️ **ACCIONES NECESARIAS EN EL SERVIDOR:**

### 1️⃣ **Verificar Variables de Entorno:**

```bash
cd /home/deploy/API-VOLTIO
cat .env
```

**Credenciales actualizadas que deben estar:**

```bash
# PostgreSQL (NUEVAS credenciales)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=voltio_db
DB_USER=voltio_user
DB_PASSWORD=HSQCx3Ajt4p^aJGC

# InfluxDB (NUEVO token)
INFLUX_URL=http://localhost:8086
INFLUX_TOKEN=F2wrepMKWQE_RQrNpKndw3r-xnVTvhj6R0-cu2gulI23YhBAE-x_V4SLnQkUzK97pdHc-4AJn7X9SSJErowPbA==
INFLUX_ORG=VOLTIO
INFLUX_BUCKET=sensor_data

# JWT (NUEVA clave secreta)
SECRET_KEY=91-character-secret-key-updated-in-local-development-environment-for-security

# SSH Tunnel
SSH_TUNNEL_ENABLED=true
```

### 2️⃣ **Verificar Conexión PostgreSQL:**

```bash
# Probar conexión directa
psql -h localhost -p 5432 -U voltio_user -d voltio_db

# Si no funciona, verificar túnel SSH
ps aux | grep ssh
```

### 3️⃣ **Verificar Túnel SSH:**

```bash
# Verificar si está corriendo
sudo supervisorctl status ssh-tunnel

# Si no está corriendo, iniciarlo
sudo supervisorctl start ssh-tunnel

# Verificar puertos
netstat -tlnp | grep 5432
```

### 4️⃣ **Verificar Logs de la Aplicación:**

```bash
# Ver logs de la aplicación
sudo supervisorctl tail -f voltio-api

# Ver logs del sistema
journalctl -u voltio-api -f
```

### 5️⃣ **Reiniciar Servicios:**

```bash
# Reiniciar túnel SSH
sudo supervisorctl restart ssh-tunnel

# Reiniciar aplicación
sudo supervisorctl restart voltio-api

# Verificar estado
sudo supervisorctl status
```

### 6️⃣ **Aplicar Credenciales Actualizadas:**

Si el archivo `.env` no tiene las credenciales correctas:

```bash
# Hacer backup del .env actual
cp .env .env.backup

# Editar con las nuevas credenciales
nano .env

# Reiniciar después de cambios
sudo supervisorctl restart voltio-api
```

## 🧪 **Verificación Post-Reparación:**

Una vez aplicadas las correcciones, probar:

```bash
# Desde el servidor
curl http://localhost:8000/api/v1/users/login -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"superadmin@voltio.com","password":"SuperAdmin123!"}'
```

Respuesta esperada:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

## 📝 **Checklist de Reparación:**

- [ ] Variables de entorno verificadas
- [ ] PostgreSQL accesible
- [ ] Túnel SSH funcionando
- [ ] InfluxDB conectado
- [ ] Aplicación reiniciada
- [ ] Login funcionando
- [ ] Endpoints autenticados respondiendo

## 🎯 **Resultado Esperado:**

Después de las correcciones, el API debe responder:

- ✅ Login exitoso (Status 200)
- ✅ Endpoints autenticados funcionando
- ✅ Comandos de relé operativos
- ✅ Lecturas PZEM funcionando

---

**Estado:** ⚠️ Requiere intervención en servidor  
**Prioridad:** 🔥 Alta - Funcionalidad crítica afectada
