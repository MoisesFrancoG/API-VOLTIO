# 📚 API VOLTIO - Documentación Completa de Endpoints

## 🌐 Información General

**URL Base Desarrollo:** `http://127.0.0.1:8000`  
**URL Base Producción:** `https://voltioapi.acstree.xyz`  
**Prefijo API:** `/api/v1`  
**Versión:** 1.2.0  
**Tipo:** RESTful API  
**Autenticación:** JWT Bearer Token

---

## 🔐 Autenticación

### Header Requerido (Endpoints Protegidos)

```http
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

### Flujo de Autenticación

1. **Login:** `POST /users/login` → Obtener `access_token`
2. **Usar Token:** Incluir en header `Authorization: Bearer {token}`
3. **Verificar:** `GET /users/me` para validar token

---

## 📋 Códigos de Respuesta HTTP

| Código  | Significado      | Contextos                               |
| ------- | ---------------- | --------------------------------------- |
| **200** | OK               | GET, PUT exitosos                       |
| **201** | Created          | POST exitoso (recurso creado)           |
| **204** | No Content       | DELETE exitoso                          |
| **400** | Bad Request      | Datos inválidos                         |
| **401** | Unauthorized     | Token inválido/faltante                 |
| **403** | Forbidden        | Sin permisos suficientes                |
| **404** | Not Found        | Recurso no encontrado                   |
| **409** | Conflict         | Recurso duplicado (ej: email ya existe) |
| **422** | Validation Error | Error de validación de campos           |
| **500** | Internal Error   | Error del servidor                      |

---

## 🎯 ENDPOINTS POR MÓDULO

## 1. 👥 USUARIOS (Users)

**Base Path:** `/api/v1/users`

### 🔓 Endpoints Públicos

#### `POST /users/register`

- **Descripción:** Registrar nuevo usuario (público)
- **Permisos:** Ninguno
- **Status:** `201 Created`
- **Body:**

```json
{
  "name": "string",
  "email": "string",
  "password": "string",
  "role_id": 2
}
```

- **Respuesta:**

```json
{
  "id": 1,
  "name": "Juan Pérez",
  "email": "juan@email.com",
  "role": {
    "id": 2,
    "name": "user"
  },
  "created_at": "2025-07-20T10:30:00"
}
```

#### `POST /users/login`

- **Descripción:** Autenticar usuario y obtener JWT token
- **Permisos:** Ninguno
- **Status:** `200 OK`
- **Body:**

```json
{
  "email": "usuario@email.com",
  "password": "password123"
}
```

- **Respuesta:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "Juan Pérez",
    "email": "usuario@email.com",
    "role": {
      "id": 2,
      "name": "user"
    }
  }
}
```

### 🔒 Endpoints Protegidos (Autenticación Requerida)

#### `GET /users/me`

- **Descripción:** Obtener información del usuario actual
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

#### `GET /users/`

- **Descripción:** Listar todos los usuarios
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

#### `GET /users/{user_id}`

- **Descripción:** Obtener usuario por ID
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

#### `GET /users/email/{email}`

- **Descripción:** Obtener usuario por email
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

#### `PUT /users/{user_id}`

- **Descripción:** Actualizar información de usuario
- **Permisos:** Propietario o Admin
- **Status:** `200 OK`
- **Body:**

```json
{
  "name": "string",
  "email": "string"
}
```

#### `PATCH /users/{user_id}/password`

- **Descripción:** Cambiar contraseña
- **Permisos:** Propietario o Admin
- **Status:** `200 OK`
- **Body:**

```json
{
  "current_password": "string",
  "new_password": "string"
}
```

### 🔒🔑 Endpoints Admin

#### `POST /users/`

- **Descripción:** Crear nuevo usuario (por admin)
- **Permisos:** Solo Admin
- **Status:** `201 Created`

#### `DELETE /users/{user_id}`

- **Descripción:** Eliminar usuario
- **Permisos:** Solo Admin
- **Status:** `204 No Content`

---

## 2. 🏷️ ROLES

**Base Path:** `/api/v1/roles`

### 🔒 Endpoints con Autenticación

#### `GET /roles/`

- **Descripción:** Listar todos los roles
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

#### `GET /roles/{role_id}`

- **Descripción:** Obtener rol por ID
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

### 🔒🔑 Endpoints Admin

#### `POST /roles/`

- **Descripción:** Crear nuevo rol
- **Permisos:** Solo Admin
- **Status:** `201 Created`
- **Body:**

```json
{
  "name": "string",
  "description": "string"
}
```

#### `PUT /roles/{role_id}`

- **Descripción:** Actualizar rol existente
- **Permisos:** Solo Admin
- **Status:** `200 OK`

#### `DELETE /roles/{role_id}`

- **Descripción:** Eliminar rol
- **Permisos:** Solo Admin
- **Status:** `204 No Content`

---

## 3. 📍 UBICACIONES (Locations)

**Base Path:** `/api/v1/locations`

### 🔒 Endpoints con Autenticación

#### `GET /locations/`

- **Descripción:** Listar todas las ubicaciones
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

#### `GET /locations/{location_id}`

- **Descripción:** Obtener ubicación por ID
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

### 🔒🔑 Endpoints Admin

#### `POST /locations/`

- **Descripción:** Crear nueva ubicación
- **Permisos:** Solo Admin
- **Status:** `201 Created`
- **Body:**

```json
{
  "name": "string",
  "description": "string",
  "address": "string"
}
```

#### `PUT /locations/{location_id}`

- **Descripción:** Actualizar ubicación
- **Permisos:** Solo Admin
- **Status:** `200 OK`

#### `DELETE /locations/{location_id}`

- **Descripción:** Eliminar ubicación
- **Permisos:** Solo Admin
- **Status:** `204 No Content`

---

## 4. 🔧 TIPOS DE DISPOSITIVOS (Device Types)

**Base Path:** `/api/v1/device-types`

### 🔒 Endpoints con Autenticación

#### `GET /device-types/`

- **Descripción:** Listar todos los tipos de dispositivos
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

#### `GET /device-types/{type_id}`

- **Descripción:** Obtener tipo de dispositivo por ID
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

### 🔒🔑 Endpoints Admin

#### `POST /device-types/`

- **Descripción:** Crear nuevo tipo de dispositivo
- **Permisos:** Solo Admin
- **Status:** `201 Created`
- **Body:**

```json
{
  "name": "string",
  "description": "string",
  "category": "string"
}
```

#### `PUT /device-types/{type_id}`

- **Descripción:** Actualizar tipo de dispositivo
- **Permisos:** Solo Admin
- **Status:** `200 OK`

#### `DELETE /device-types/{type_id}`

- **Descripción:** Eliminar tipo de dispositivo
- **Permisos:** Solo Admin
- **Status:** `204 No Content`

---

## 5. 🔌 DISPOSITIVOS (Devices)

**Base Path:** `/api/v1/devices`

### 🔒 Endpoints con Autenticación

#### `POST /devices/` ⭐

- **Descripción:** Crear nuevo dispositivo
- **Permisos:** Usuario autenticado
- **Status:** `201 Created` (⚠️ Recientemente corregido)
- **Body:**

```json
{
  "name": "string",
  "mac_address": "AA:BB:CC:DD:EE:FF",
  "device_type_id": 1,
  "location_id": 1,
  "description": "string",
  "is_active": true
}
```

- **Respuesta:**

```json
{
  "id": 1,
  "name": "Mi ESP32",
  "mac_address": "AA:BB:CC:DD:EE:FF",
  "device_type_id": 1,
  "location_id": 1,
  "description": "Dispositivo IoT",
  "is_active": true,
  "user_id": 1,
  "created_at": "2025-07-20T10:30:00"
}
```

#### `GET /devices/`

- **Descripción:** Listar todos los dispositivos
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`
- **Query Params:**
  - `active_only` (bool): Solo dispositivos activos
  - `skip` (int): Número de registros a saltar
  - `limit` (int): Límite de registros

#### `GET /devices/{device_id}`

- **Descripción:** Obtener dispositivo por ID
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

#### `GET /devices/type/{device_type_id}`

- **Descripción:** Obtener dispositivos por tipo
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

#### `GET /devices/location/{location_id}`

- **Descripción:** Obtener dispositivos por ubicación
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

#### `GET /devices/user/{user_id}`

- **Descripción:** Obtener dispositivos de un usuario
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

#### `PUT /devices/{device_id}`

- **Descripción:** Actualizar dispositivo
- **Permisos:** Propietario del dispositivo
- **Status:** `200 OK`

#### `DELETE /devices/{device_id}`

- **Descripción:** Eliminar dispositivo
- **Permisos:** Propietario del dispositivo
- **Status:** `204 No Content`

---

## 6. ⚡ COMANDO DE RELÉ

**Base Path:** `/api/v1/devices`

#### `POST /devices/{mac_address}/command/relay`

- **Descripción:** Enviar comando de relé a dispositivo ESP32
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`
- **Path Params:**
  - `mac_address`: Dirección MAC del dispositivo
- **Body:**

```json
{
  "action": "on" // "on", "off", "toggle"
}
```

- **Respuesta:**

```json
{
  "status": "success",
  "message": "Comando enviado exitosamente",
  "device_mac": "AA:BB:CC:DD:EE:FF",
  "command": "relay_on",
  "timestamp": "2025-07-20T10:30:00"
}
```

- **Errores Comunes:**
  - `404`: Dispositivo no encontrado
  - `409`: Dispositivo no es del tipo correcto (debe ser NODO_CONTROL_PZEM)

---

## 7. 📡 COMANDOS IR (Infrared Commands)

**Base Path:** `/api/v1/device-commands`

### 🔒 Endpoints con Autenticación

#### `GET /device-commands/`

- **Descripción:** Listar todos los comandos IR
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`
- **Query Params:**
  - `skip` (int): Número de registros a saltar
  - `limit` (int): Límite de registros
  - `device_id` (int): Filtrar por dispositivo

#### `GET /device-commands/{command_id}`

- **Descripción:** Obtener comando IR por ID
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

#### `GET /device-commands/device/{device_id}`

- **Descripción:** Obtener comandos IR de un dispositivo
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

#### `POST /device-commands/`

- **Descripción:** Crear nuevo comando IR
- **Permisos:** Usuario autenticado
- **Status:** `201 Created`
- **Body:**

```json
{
  "device_id": 1,
  "command_name": "string",
  "command_type": "string",
  "command_data": "string",
  "description": "string"
}
```

#### `PUT /device-commands/{command_id}`

- **Descripción:** Actualizar comando IR
- **Permisos:** Propietario del comando
- **Status:** `200 OK`

#### `DELETE /device-commands/{command_id}`

- **Descripción:** Eliminar comando IR
- **Permisos:** Propietario del comando
- **Status:** `204 No Content`

---

## 8. 📊 LECTURAS PZEM (Energy Readings)

**Base Path:** `/api/v1/lecturas-pzem`

### 🔒 Endpoints con Autenticación

#### `GET /lecturas-pzem/{time_range}`

- **Descripción:** Obtener lecturas por rango de tiempo
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`
- **Path Params:**
  - `time_range`: `last_hour`, `last_day`, `last_week`, `last_month`
- **Query Params:**
  - `device_mac` (string): MAC del dispositivo
  - `limit` (int): Número máximo de lecturas

#### `GET /lecturas-pzem/device/{device_mac}`

- **Descripción:** Obtener lecturas de un dispositivo específico
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`
- **Query Params:**
  - `limit` (int): Número máximo de lecturas
  - `start_date` (datetime): Fecha inicio
  - `end_date` (datetime): Fecha fin

#### `GET /lecturas-pzem/stats/{device_mac}`

- **Descripción:** Obtener estadísticas de consumo
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

- **Respuesta Típica:**

```json
[
  {
    "id": "abc123",
    "device_mac": "AA:BB:CC:DD:EE:FF",
    "voltage": 220.5,
    "current": 1.25,
    "power": 275.6,
    "energy": 1.5,
    "frequency": 50.0,
    "power_factor": 0.95,
    "timestamp": "2025-07-20T10:30:00"
  }
]
```

---

## 9. 🔔 NOTIFICACIONES

**Base Path:** `/api/v1/notifications`

### 🔒 Endpoints con Autenticación

#### `GET /notifications/`

- **Descripción:** Listar notificaciones del usuario
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`
- **Query Params:**
  - `skip` (int): Registros a saltar
  - `limit` (int): Máximo registros
  - `unread_only` (bool): Solo no leídas

#### `GET /notifications/{notification_id}`

- **Descripción:** Obtener notificación por ID
- **Permisos:** Propietario de la notificación
- **Status:** `200 OK`

#### `POST /notifications/`

- **Descripción:** Crear nueva notificación
- **Permisos:** Usuario autenticado
- **Status:** `201 Created`
- **Body:**

```json
{
  "title": "string",
  "message": "string",
  "notification_type": "info", // "info", "warning", "error", "success"
  "related_device_id": 1,
  "expires_at": "2025-07-25T10:30:00"
}
```

#### `PUT /notifications/{notification_id}/read`

- **Descripción:** Marcar notificación como leída
- **Permisos:** Propietario de la notificación
- **Status:** `200 OK`

#### `DELETE /notifications/{notification_id}`

- **Descripción:** Eliminar notificación
- **Permisos:** Propietario de la notificación
- **Status:** `204 No Content`

#### `DELETE /notifications/all`

- **Descripción:** Eliminar todas las notificaciones del usuario
- **Permisos:** Usuario autenticado
- **Status:** `204 No Content`

---

## 10. 🔔 SERVICIO DE NOTIFICACIONES

**Base Path:** `/api/v1/notifications`

### 🔒 Endpoints con Autenticación

#### `POST /notifications/service`

- **Descripción:** Crear notificación de servicio
- **Permisos:** Usuario autenticado
- **Status:** `201 Created`

#### `POST /notifications/service/sync`

- **Descripción:** Sincronizar notificaciones
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

#### `POST /notifications/manual`

- **Descripción:** Enviar notificación manual
- **Permisos:** Usuario autenticado
- **Status:** `201 Created`

#### `PUT /notifications/bulk-read`

- **Descripción:** Marcar múltiples como leídas
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`
- **Body:**

```json
{
  "notification_ids": [1, 2, 3, 4, 5]
}
```

#### `GET /notifications/health`

- **Descripción:** Estado del servicio de notificaciones
- **Permisos:** Usuario autenticado
- **Status:** `200 OK`

---

## 🧪 ENDPOINTS DE PRUEBA Y MONITOREO

**Base Path:** `/test`

### 🔓 Endpoints Públicos

#### `GET /` (Root)

- **Descripción:** Endpoint raíz de la API
- **Status:** `200 OK`

#### `GET /test/quick`

- **Descripción:** Verificación rápida
- **Status:** `200 OK`

#### `GET /test/health`

- **Descripción:** Health check estándar
- **Status:** `200 OK`

#### `GET /test/deployment`

- **Descripción:** Información completa de despliegue
- **Status:** `200 OK`

#### `GET /test/deployment-v2`

- **Descripción:** Información de despliegue v2
- **Status:** `200 OK`

#### `GET /test/system-info`

- **Descripción:** Información detallada del sistema
- **Status:** `200 OK`

#### `GET /test/database-check`

- **Descripción:** Verificación de bases de datos
- **Status:** `200 OK`

#### `GET /test/environment-vars`

- **Descripción:** Variables de entorno (sin secretos)
- **Status:** `200 OK`

#### `GET /test/api-performance`

- **Descripción:** Test de rendimiento básico
- **Status:** `200 OK`

#### `GET /test/all-endpoints`

- **Descripción:** Resumen de todos los endpoints de prueba
- **Status:** `200 OK`

---

## 🎯 FLUJOS DE TRABAJO TÍPICOS

### 🚀 1. Autenticación y Setup Inicial

```bash
# 1. Login
POST /users/login

# 2. Verificar usuario
GET /users/me

# 3. Obtener datos maestros
GET /locations/
GET /device-types/
GET /roles/
```

### 🏠 2. Dashboard Principal

```bash
# Obtener dispositivos del usuario
GET /devices/user/{user_id}

# Obtener notificaciones no leídas
GET /notifications/?unread_only=true&limit=10

# Obtener lecturas recientes
GET /lecturas-pzem/last_hour
```

### 🔌 3. Gestión de Dispositivos

```bash
# Crear dispositivo
POST /devices/

# Listar mis dispositivos
GET /devices/user/{user_id}

# Controlar relé
POST /devices/{mac}/command/relay

# Ver historial energético
GET /lecturas-pzem/device/{mac}
```

### 🔧 4. Administración (Solo Admin)

```bash
# Crear ubicación
POST /locations/

# Crear tipo de dispositivo
POST /device-types/

# Gestionar usuarios
GET /users/
POST /users/
PUT /users/{id}
```

---

## 💡 CONSIDERACIONES IMPORTANTES

### 🔒 Seguridad

- Todos los endpoints protegidos requieren JWT token válido
- Los tokens expiran después de 30 minutos (configurable)
- Los usuarios solo pueden modificar sus propios recursos (excepto admins)
- Las contraseñas se almacenan hasheadas con bcrypt

### ⚡ Rendimiento

- Usa paginación en endpoints que retornan listas grandes
- Los endpoints de lecturas PZEM pueden ser lentos con grandes rangos de tiempo
- Implementa límites de rate limiting en producción

### 🐛 Manejo de Errores

- Todos los endpoints retornan JSON structures consistentes
- Los errores incluyen códigos HTTP apropiados y mensajes descriptivos
- Validación automática de schemas con FastAPI/Pydantic

### 📊 Monitoreo

- Usa los endpoints `/test/*` para health checks
- Monitorea el endpoint `/test/database-check` para conectividad DB
- Los logs incluyen información de requests y errores

---

## 🔗 Recursos Adicionales

### 📚 Documentación Interactiva

- **Swagger UI:** `{base_url}/docs`
- **ReDoc:** `{base_url}/redoc`
- **OpenAPI JSON:** `{base_url}/openapi.json`

### 🌐 URLs de Producción

- **API:** `https://voltioapi.acstree.xyz/api/v1`
- **Docs:** `https://voltioapi.acstree.xyz/docs`
- **Health:** `https://voltioapi.acstree.xyz/test/health`

### 🛠️ Herramientas de Testing

- Postman Collection disponible
- Scripts de testing automatizado incluidos
- Ejemplos de código en JavaScript/Python disponibles

---

**📝 Nota:** Esta documentación cubre la versión 1.2.0 del API. Para actualizaciones y cambios, consultar el changelog en el repositorio.
