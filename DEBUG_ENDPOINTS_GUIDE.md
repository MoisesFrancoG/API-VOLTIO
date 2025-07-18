# 🔧 Endpoints de Desarrollo para Pruebas - API Voltio

## 📋 Resumen

Para facilitar las pruebas de la API Voltio, se han agregado endpoints especiales de desarrollo que permiten obtener tokens JWT fácilmente sin necesidad de hacer login manual.

## 🚨 Importante

⚠️ **Estos endpoints SOLO funcionan en modo desarrollo** (`ENVIRONMENT=development`)
⚠️ **NO están disponibles en producción por razones de seguridad**

## 🔑 Endpoints Disponibles

### 1. Obtener Token JWT
```
GET /debug/token?user_email={email}
```

**Parámetros:**
- `user_email` (opcional): Email del usuario. Por defecto: "admin@voltio.com"

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user_info": {
    "id": 7,
    "nombre": "Administrador", 
    "email": "admin@voltio.com",
    "rol_id": 1
  },
  "usage": "Authorization: Bearer eyJhbGciOiJIUzI1NiIs...",
  "note": "Este token es solo para desarrollo y pruebas"
}
```

### 2. Listar Usuarios Disponibles
```
GET /debug/users
```

**Respuesta:**
```json
{
  "users": [
    {
      "id": 7,
      "nombre": "Administrador",
      "email": "admin@voltio.com", 
      "rol": "admin"
    },
    {
      "id": 8,
      "nombre": "mike",
      "email": "miketrike445646@example.com",
      "rol": "admin"
    }
  ],
  "total": 2,
  "usage": "Usa /debug/token?user_email=EMAIL para obtener token de cualquier usuario"
}
```

## 🛠️ Herramientas de Prueba

### Script PowerShell
Se incluye un script `get_token.ps1` para facilitar las pruebas:

```powershell
# Obtener token para administrador
.\get_token.ps1

# Obtener token para otro usuario
.\get_token.ps1 -UserEmail "miketrike445646@example.com"
```

### Uso Manual con PowerShell

```powershell
# 1. Obtener token
$response = Invoke-RestMethod -Uri "http://localhost:8000/debug/token" -Method Get

# 2. Configurar headers
$headers = @{ "Authorization" = "Bearer $($response.access_token)" }

# 3. Usar en peticiones
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/usuarios/me" -Method Get -Headers $headers
```

### Uso con curl

```bash
# 1. Obtener token
curl http://localhost:8000/debug/token

# 2. Usar token en peticiones
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/v1/usuarios/me
```

## 📊 Ejemplos de Pruebas

### Probar diferentes endpoints:

```powershell
# Obtener token
$response = Invoke-RestMethod -Uri "http://localhost:8000/debug/token" -Method Get
$headers = @{ "Authorization" = "Bearer $($response.access_token)" }

# Listar usuarios
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/usuarios/" -Method Get -Headers $headers

# Listar sensores  
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sensores/" -Method Get -Headers $headers

# Crear nuevo sensor
$nuevoSensor = @{
    nombre = "Sensor Prueba"
    descripcion = "Sensor de prueba para testing"
    id_tipo_sensor = 1
    id_ubicacion = 1
    id_usuario = 7
    activo = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/sensores/" -Method Post -Body $nuevoSensor -Headers $headers -ContentType "application/json"
```

## 🎯 Casos de Uso

1. **Desarrollo Local**: Obtener tokens rápidamente para probar endpoints
2. **Testing Automatizado**: Scripts pueden obtener tokens sin login manual
3. **Debugging**: Probar con diferentes usuarios y roles
4. **Integración**: Facilitar pruebas de integración con sistemas externos

## 🔒 Seguridad

- Los endpoints solo funcionan en modo `development`
- Los tokens tienen la misma duración que los tokens normales (30 minutos por defecto)
- Se requiere que el usuario exista en la base de datos
- Los tokens generados son idénticos a los obtenidos por login normal

## 📝 Logs y Monitoreo

Los endpoints de debug aparecen en los logs de la API como cualquier otra petición, facilitando el debugging y monitoreo durante el desarrollo.

---

✅ **La API Voltio ahora es mucho más fácil de probar y desarrollar!** 🚀
