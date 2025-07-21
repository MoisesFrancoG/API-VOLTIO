# 📚 API VOLTIO - Documentación Completa para Frontend

## 🌐 Información General

**URL Base:** `http://127.0.0.1:8000`  
**Versión:** 1.0.0  
**Prefijo API:** `/api/v1`

## 🔐 Autenticación

Todos los endpoints (excepto login/register) requieren autenticación JWT.

**Header requerido:**
```http
Authorization: Bearer {jwt_token}
```

**Cómo obtener token:**
1. POST `/api/v1/users/login` con email/password
2. Usar el `access_token` de la respuesta

---

## 👥 USUARIOS (Users)

### 🔓 Registro de Usuario
```http
POST /api/v1/users/register
```

**Body:**
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string",
  "role_id": 2
}
```

**Respuesta (201):**
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "role_id": 2,
  "created_at": "2025-01-20T10:00:00"
}
```

### 🔓 Login
```http
POST /api/v1/users/login
```

**Body:**
```json
{
  "email": "user@example.com",
  "password": "string"
}
```

**Respuesta (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "string",
    "email": "user@example.com",
    "role_id": 2
  }
}
```

### 🔒 Obtener Todos los Usuarios
```http
GET /api/v1/users/
```

**Permisos:** Cualquier usuario autenticado

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "username": "string",
    "email": "user@example.com",
    "role_id": 2,
    "created_at": "2025-01-20T10:00:00"
  }
]
```

### 🔒 Obtener Usuario Actual
```http
GET /api/v1/users/me
```

**Respuesta (200):**
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "role_id": 2,
  "created_at": "2025-01-20T10:00:00"
}
```

### 🔒 Obtener Usuario por ID
```http
GET /api/v1/users/{user_id}
```

**Respuesta (200):**
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "role_id": 2,
  "created_at": "2025-01-20T10:00:00"
}
```

### 🔒 Actualizar Usuario
```http
PUT /api/v1/users/{user_id}
```

**Body:**
```json
{
  "username": "new_username",
  "email": "newemail@example.com",
  "role_id": 2
}
```

### 🔒 Cambiar Contraseña
```http
POST /api/v1/users/change-password
```

**Body:**
```json
{
  "current_password": "old_password",
  "new_password": "new_password"
}
```

### 🔒 Eliminar Usuario
```http
DELETE /api/v1/users/{user_id}
```

**Permisos:** Solo el propio usuario o admin

---

## 🏷️ ROLES

### 🔒 Obtener Todos los Roles
```http
GET /api/v1/roles/
```

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "name": "ADMIN",
    "description": "Administrator role"
  },
  {
    "id": 2,
    "name": "USER",
    "description": "Regular user role"
  }
]
```

### 🔒 Obtener Rol por ID
```http
GET /api/v1/roles/{role_id}
```

### 🔒🔑 Crear Rol
```http
POST /api/v1/roles/
```

**Permisos:** Solo Admin

**Body:**
```json
{
  "name": "MODERATOR",
  "description": "Moderator role"
}
```

### 🔒🔑 Actualizar Rol
```http
PUT /api/v1/roles/{role_id}
```

**Permisos:** Solo Admin

### 🔒🔑 Eliminar Rol
```http
DELETE /api/v1/roles/{role_id}
```

**Permisos:** Solo Admin

---

## 📍 UBICACIONES (Locations)

### 🔒 Obtener Todas las Ubicaciones
```http
GET /api/v1/locations/
```

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "name": "Oficina Principal",
    "description": "Ubicación principal del edificio"
  }
]
```

### 🔒 Obtener Ubicación por ID
```http
GET /api/v1/locations/{location_id}
```

### 🔒🔑 Crear Ubicación
```http
POST /api/v1/locations/
```

**Permisos:** Solo Admin

**Body:**
```json
{
  "name": "Nueva Oficina",
  "description": "Descripción de la ubicación"
}
```

### 🔒🔑 Actualizar Ubicación
```http
PUT /api/v1/locations/{location_id}
```

**Permisos:** Solo Admin

### 🔒🔑 Eliminar Ubicación
```http
DELETE /api/v1/locations/{location_id}
```

**Permisos:** Solo Admin

---

## 🔧 TIPOS DE DISPOSITIVOS (Device Types)

### 🔒 Obtener Todos los Tipos
```http
GET /api/v1/device-types/
```

**Respuesta (200):**
```json
[
  {
    "id": 5,
    "type_name": "NODO_CONTROL_PZEM",
    "description": "Dispositivo de control con relé"
  },
  {
    "id": 6,
    "type_name": "NODO_SENSADO_RPI",
    "description": "Dispositivo de sensado Raspberry Pi"
  }
]
```

### 🔒 Obtener Tipo por ID
```http
GET /api/v1/device-types/{device_type_id}
```

### 🔒🔑 Crear Tipo de Dispositivo
```http
POST /api/v1/device-types/
```

**Permisos:** Solo Admin

**Body:**
```json
{
  "type_name": "NUEVO_TIPO",
  "description": "Descripción del nuevo tipo"
}
```

### 🔒🔑 Actualizar Tipo
```http
PUT /api/v1/device-types/{device_type_id}
```

**Permisos:** Solo Admin

### 🔒🔑 Eliminar Tipo
```http
DELETE /api/v1/device-types/{device_type_id}
```

**Permisos:** Solo Admin

---

## 🔌 DISPOSITIVOS (Devices)

### 🔒 Crear Dispositivo
```http
POST /api/v1/devices/
```

**Body:**
```json
{
  "name": "Mi Dispositivo",
  "mac_address": "AA:BB:CC:DD:EE:FF",
  "device_type_id": 5,
  "location_id": 1,
  "description": "Descripción del dispositivo"
}
```

**Respuesta (201):**
```json
{
  "id": 1,
  "name": "Mi Dispositivo",
  "mac_address": "AA:BB:CC:DD:EE:FF",
  "device_type_id": 5,
  "location_id": 1,
  "user_id": 1,
  "description": "Descripción del dispositivo",
  "created_at": "2025-01-20T10:00:00"
}
```

### 🔒 Obtener Dispositivo por ID
```http
GET /api/v1/devices/{device_id}
```

### 🔒 Obtener Todos los Dispositivos
```http
GET /api/v1/devices/
```

**Query Parameters:**
- `skip`: Número de registros a saltar (default: 0)
- `limit`: Número máximo de registros (default: 100)

### 🔒 Dispositivos por Tipo
```http
GET /api/v1/devices/type/{device_type_id}
```

### 🔒 Dispositivos por Ubicación
```http
GET /api/v1/devices/location/{location_id}
```

### 🔒 Dispositivos por Usuario
```http
GET /api/v1/devices/user/{user_id}
```

### 🔒 Buscar Dispositivos
```http
GET /api/v1/devices/search/?q={search_term}
```

**Query Parameters:**
- `q`: Término de búsqueda (busca en nombre, MAC, descripción)

### 🔒 Actualizar Dispositivo
```http
PUT /api/v1/devices/{device_id}
```

**Permisos:** Solo el propietario del dispositivo

**Body:**
```json
{
  "name": "Nuevo Nombre",
  "description": "Nueva descripción",
  "location_id": 2
}
```

### 🔒 Eliminar Dispositivo
```http
DELETE /api/v1/devices/{device_id}
```

**Permisos:** Solo el propietario del dispositivo

---

## ⚡ COMANDO DE RELÉ (Relay Command)

### 🔒 Enviar Comando de Relé
```http
POST /api/v1/devices/{mac_address}/command/relay
```

**Permisos:** Solo el propietario del dispositivo

**Body:**
```json
{
  "action": "ON"
}
```

**Valores permitidos para action:**
- `"ON"`: Encender relé
- `"OFF"`: Apagar relé

**Respuesta (202):**
```json
{
  "status": "Comando de relé enviado al dispositivo",
  "device_mac": "AA:BB:CC:DD:EE:FF",
  "action_sent": "ON"
}
```

**Errores posibles:**
- `400`: Comando inválido
- `401`: No autenticado
- `403`: No es propietario del dispositivo
- `404`: Dispositivo no encontrado
- `409`: Dispositivo no es tipo NODO_CONTROL_PZEM
- `500`: Error interno del servidor

---

## 📡 COMANDOS IR (Device Commands)

### 🔒 Obtener Todos los Comandos
```http
GET /api/v1/device-commands/
```

### 🔒 Obtener Comando por ID
```http
GET /api/v1/device-commands/{command_id}
```

### 🔒 Buscar Comandos
```http
GET /api/v1/device-commands/search/?device={device_name}&command={command_name}
```

### 🔒🔑 Crear Comando IR
```http
POST /api/v1/device-commands/
```

**Permisos:** Solo Admin

**Body:**
```json
{
  "device_capability_instance_id": 1,
  "device_name": "TV Samsung",
  "command_name": "POWER",
  "ir_code": "FF00FF00FF00FF00",
  "description": "Comando de encendido"
}
```

### 🔒🔑 Actualizar Comando
```http
PUT /api/v1/device-commands/{command_id}
```

**Permisos:** Solo Admin

### 🔒🔑 Eliminar Comando
```http
DELETE /api/v1/device-commands/{command_id}
```

**Permisos:** Solo Admin

---

## 📊 LECTURAS PZEM

### 🔒 Obtener Lecturas
```http
GET /api/v1/lecturas-pzem/
```

**Query Parameters:**
- `device_mac`: MAC del dispositivo
- `start_time`: Tiempo inicial (ISO format)
- `end_time`: Tiempo final (ISO format)
- `limit`: Número máximo de registros

**Respuesta (200):**
```json
[
  {
    "time": "2025-01-20T10:00:00Z",
    "device_mac": "AA:BB:CC:DD:EE:FF",
    "voltage": 220.5,
    "current": 1.2,
    "power": 264.6,
    "energy": 1000.0,
    "frequency": 60.0,
    "power_factor": 0.95
  }
]
```

---

## 🔔 NOTIFICACIONES

### 🔒 Obtener Mis Notificaciones
```http
GET /api/v1/notifications/
```

**Query Parameters:**
- `skip`: Registros a saltar
- `limit`: Máximo de registros
- `unread_only`: Solo no leídas (true/false)

### 🔒 Obtener Notificación por ID
```http
GET /api/v1/notifications/{notification_id}
```

### 🔒 Crear Notificación
```http
POST /api/v1/notifications/
```

**Body:**
```json
{
  "title": "Título de la notificación",
  "message": "Mensaje de la notificación",
  "type": "INFO",
  "user_id": 1
}
```

**Tipos disponibles:**
- `"INFO"`: Información
- `"WARNING"`: Advertencia
- `"ERROR"`: Error
- `"SUCCESS"`: Éxito

### 🔒 Marcar como Leída
```http
PUT /api/v1/notifications/{notification_id}/read
```

### 🔒 Eliminar Notificación
```http
DELETE /api/v1/notifications/{notification_id}
```

### 🔒 Eliminar Todas las Notificaciones
```http
DELETE /api/v1/notifications/all
```

---

## 🔔 SERVICIO DE NOTIFICACIONES

### 🔒 Notificación de Servicio
```http
POST /notifications/service
```

**Body:**
```json
{
  "device_mac": "AA:BB:CC:DD:EE:FF",
  "message": "Mensaje de servicio",
  "severity": "INFO"
}
```

### 🔒 Sincronización de Notificaciones
```http
POST /notifications/service/sync
```

### 🔒 Notificación Manual
```http
POST /notifications/manual
```

### 🔒 Marcar Múltiples como Leídas
```http
PUT /notifications/bulk-read
```

### 🔒 Estado del Servicio
```http
GET /notifications/health
```

---

## 📝 Ejemplos de Uso Frontend

### Autenticación Completa
```javascript
// 1. Login
const loginResponse = await fetch('/api/v1/users/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});

const { access_token } = await loginResponse.json();

// 2. Usar token en requests subsecuentes
const authHeaders = {
  'Authorization': `Bearer ${access_token}`,
  'Content-Type': 'application/json'
};
```

### Gestión de Dispositivos
```javascript
// Crear dispositivo
const createDevice = await fetch('/api/v1/devices/', {
  method: 'POST',
  headers: authHeaders,
  body: JSON.stringify({
    name: 'Mi ESP32',
    mac_address: 'AA:BB:CC:DD:EE:FF',
    device_type_id: 5,
    location_id: 1,
    description: 'Dispositivo de control'
  })
});

// Enviar comando de relé
const relayCommand = await fetch('/api/v1/devices/AA:BB:CC:DD:EE:FF/command/relay', {
  method: 'POST',
  headers: authHeaders,
  body: JSON.stringify({
    action: 'ON'
  })
});
```

### Obtener Datos
```javascript
// Obtener dispositivos del usuario
const devices = await fetch('/api/v1/devices/', {
  headers: authHeaders
});

// Obtener lecturas de un dispositivo
const readings = await fetch('/api/v1/lecturas-pzem/?device_mac=AA:BB:CC:DD:EE:FF&limit=100', {
  headers: authHeaders
});

// Obtener notificaciones
const notifications = await fetch('/api/v1/notifications/?unread_only=true', {
  headers: authHeaders
});
```

---

## 🚨 Códigos de Error Comunes

| Código | Descripción |
|--------|-------------|
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Token inválido o faltante |
| 403 | Forbidden - Sin permisos |
| 404 | Not Found - Recurso no encontrado |
| 409 | Conflict - Conflicto (ej: MAC duplicada) |
| 422 | Unprocessable Entity - Errores de validación |
| 500 | Internal Server Error - Error del servidor |

---

## 🔑 Sistema de Permisos

### Roles Disponibles:
- **Admin (role_id: 1)**: Acceso completo
- **User (role_id: 2)**: Acceso limitado

### Permisos por Módulo:
- **👥 Usuarios**: Todos pueden leer, solo propietario/admin puede modificar
- **🏷️ Roles**: Solo admin puede crear/modificar/eliminar
- **📍 Ubicaciones**: Solo admin puede crear/modificar/eliminar
- **🔧 Tipos de Dispositivos**: Solo admin puede crear/modificar/eliminar
- **🔌 Dispositivos**: Todos pueden crear, solo propietario puede modificar
- **⚡ Comandos de Relé**: Solo propietario del dispositivo
- **📡 Comandos IR**: Solo admin puede crear/modificar/eliminar
- **🔔 Notificaciones**: Cada usuario ve solo las suyas

---

## 🔄 Flujo Típico de la Aplicación

1. **Registro/Login** → Obtener token JWT
2. **Crear Dispositivo** → Registrar ESP32 con su MAC
3. **Configurar Ubicación** → Asignar ubicación al dispositivo
4. **Enviar Comandos** → Controlar relé del ESP32
5. **Monitorear Lecturas** → Ver datos de consumo
6. **Gestionar Notificaciones** → Recibir alertas del sistema

Esta documentación cubre todos los endpoints disponibles en la API Voltio. Para más detalles sobre validaciones específicas, consultar los esquemas Pydantic en cada módulo.
