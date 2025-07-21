# 📋 API VOLTIO - Referencia Rápida de Endpoints

## 🌐 Base URL: `http://127.0.0.1:8000/api/v1`

---

## 🔓 Endpoints Públicos (Sin Autenticación)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/users/register` | Registrar nuevo usuario |
| `POST` | `/users/login` | Iniciar sesión |

---

## 👥 USUARIOS

| Método | Endpoint | Permisos | Descripción |
|--------|----------|----------|-------------|
| `GET` | `/users/` | 🔒 Auth | Obtener todos los usuarios |
| `GET` | `/users/me` | 🔒 Auth | Obtener usuario actual |
| `GET` | `/users/{id}` | 🔒 Auth | Obtener usuario por ID |
| `PUT` | `/users/{id}` | 🔒 Propietario/Admin | Actualizar usuario |
| `POST` | `/users/change-password` | 🔒 Auth | Cambiar contraseña |
| `DELETE` | `/users/{id}` | 🔒 Propietario/Admin | Eliminar usuario |

---

## 🏷️ ROLES

| Método | Endpoint | Permisos | Descripción |
|--------|----------|----------|-------------|
| `GET` | `/roles/` | 🔒 Auth | Obtener todos los roles |
| `GET` | `/roles/{id}` | 🔒 Auth | Obtener rol por ID |
| `POST` | `/roles/` | 🔒🔑 Admin | Crear nuevo rol |
| `PUT` | `/roles/{id}` | 🔒🔑 Admin | Actualizar rol |
| `DELETE` | `/roles/{id}` | 🔒🔑 Admin | Eliminar rol |

---

## 📍 UBICACIONES

| Método | Endpoint | Permisos | Descripción |
|--------|----------|----------|-------------|
| `GET` | `/locations/` | 🔒 Auth | Obtener todas las ubicaciones |
| `GET` | `/locations/{id}` | 🔒 Auth | Obtener ubicación por ID |
| `POST` | `/locations/` | 🔒🔑 Admin | Crear nueva ubicación |
| `PUT` | `/locations/{id}` | 🔒🔑 Admin | Actualizar ubicación |
| `DELETE` | `/locations/{id}` | 🔒🔑 Admin | Eliminar ubicación |

---

## 🔧 TIPOS DE DISPOSITIVOS

| Método | Endpoint | Permisos | Descripción |
|--------|----------|----------|-------------|
| `GET` | `/device-types/` | 🔒 Auth | Obtener todos los tipos |
| `GET` | `/device-types/{id}` | 🔒 Auth | Obtener tipo por ID |
| `POST` | `/device-types/` | 🔒🔑 Admin | Crear nuevo tipo |
| `PUT` | `/device-types/{id}` | 🔒🔑 Admin | Actualizar tipo |
| `DELETE` | `/device-types/{id}` | 🔒🔑 Admin | Eliminar tipo |

---

## 🔌 DISPOSITIVOS

| Método | Endpoint | Permisos | Descripción |
|--------|----------|----------|-------------|
| `POST` | `/devices/` | 🔒 Auth | Crear dispositivo |
| `GET` | `/devices/` | 🔒 Auth | Obtener todos los dispositivos |
| `GET` | `/devices/{id}` | 🔒 Auth | Obtener dispositivo por ID |
| `PUT` | `/devices/{id}` | 🔒 Propietario | Actualizar dispositivo |
| `DELETE` | `/devices/{id}` | 🔒 Propietario | Eliminar dispositivo |
| `GET` | `/devices/type/{type_id}` | 🔒 Auth | Dispositivos por tipo |
| `GET` | `/devices/location/{location_id}` | 🔒 Auth | Dispositivos por ubicación |
| `GET` | `/devices/user/{user_id}` | 🔒 Auth | Dispositivos por usuario |
| `GET` | `/devices/search/?q={term}` | 🔒 Auth | Buscar dispositivos |

---

## ⚡ COMANDO DE RELÉ

| Método | Endpoint | Permisos | Descripción |
|--------|----------|----------|-------------|
| `POST` | `/devices/{mac}/command/relay` | 🔒 Propietario | Enviar comando ON/OFF |

**Body:**
```json
{ "action": "ON" }  // "ON" | "OFF"
```

---

## 📡 COMANDOS IR

| Método | Endpoint | Permisos | Descripción |
|--------|----------|----------|-------------|
| `GET` | `/device-commands/` | 🔒 Auth | Obtener todos los comandos |
| `GET` | `/device-commands/{id}` | 🔒 Auth | Obtener comando por ID |
| `GET` | `/device-commands/search/` | 🔒 Auth | Buscar comandos |
| `POST` | `/device-commands/` | 🔒🔑 Admin | Crear comando IR |
| `PUT` | `/device-commands/{id}` | 🔒🔑 Admin | Actualizar comando |
| `DELETE` | `/device-commands/{id}` | 🔒🔑 Admin | Eliminar comando |

---

## 📊 LECTURAS PZEM

| Método | Endpoint | Permisos | Descripción |
|--------|----------|----------|-------------|
| `GET` | `/lecturas-pzem/` | 🔒 Auth | Obtener lecturas |

**Query Parameters:**
- `device_mac`: MAC del dispositivo (requerido)
- `start_time`: Fecha inicio (ISO format)
- `end_time`: Fecha fin (ISO format)
- `limit`: Máximo registros (default: 1000)

---

## 🔔 NOTIFICACIONES

| Método | Endpoint | Permisos | Descripción |
|--------|----------|----------|-------------|
| `GET` | `/notifications/` | 🔒 Auth | Obtener mis notificaciones |
| `GET` | `/notifications/{id}` | 🔒 Propietario | Obtener notificación por ID |
| `POST` | `/notifications/` | 🔒 Auth | Crear notificación |
| `PUT` | `/notifications/{id}/read` | 🔒 Propietario | Marcar como leída |
| `DELETE` | `/notifications/{id}` | 🔒 Propietario | Eliminar notificación |
| `DELETE` | `/notifications/all` | 🔒 Auth | Eliminar todas mis notificaciones |

**Query Parameters para GET:**
- `skip`: Registros a saltar
- `limit`: Máximo registros
- `unread_only`: Solo no leídas (true/false)

---

## 🔔 SERVICIO DE NOTIFICACIONES

| Método | Endpoint | Permisos | Descripción |
|--------|----------|----------|-------------|
| `POST` | `/notifications/service` | 🔒 Auth | Notificación de servicio |
| `POST` | `/notifications/service/sync` | 🔒 Auth | Sincronizar notificaciones |
| `POST` | `/notifications/manual` | 🔒 Auth | Enviar notificación manual |
| `PUT` | `/notifications/bulk-read` | 🔒 Auth | Marcar múltiples como leídas |
| `GET` | `/notifications/health` | 🔒 Auth | Estado del servicio |

---

## 🎯 Endpoints Más Usados para Frontend

### 🚀 Flujo de Login
```bash
POST /users/login
GET  /users/me
```

### 🏠 Dashboard Principal
```bash
GET  /devices/
GET  /notifications/?unread_only=true
GET  /locations/
GET  /device-types/
```

### 🔌 Gestión de Dispositivos
```bash
POST /devices/                          # Crear
GET  /devices/user/{user_id}            # Mis dispositivos
PUT  /devices/{id}                      # Actualizar
POST /devices/{mac}/command/relay       # Controlar relé
```

### 📊 Monitoreo
```bash
GET /lecturas-pzem/?device_mac={mac}&limit=100
```

### 🔧 Administración (Solo Admin)
```bash
POST /locations/                        # Crear ubicación
POST /device-types/                     # Crear tipo
POST /roles/                           # Crear rol
```

---

## 🔑 Autenticación Headers

Todos los endpoints marcados con 🔒 requieren:

```http
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

---

## 📋 Códigos de Respuesta Comunes

| Código | Significado | Cuándo Ocurre |
|--------|-------------|---------------|
| `200` | OK | Operación exitosa |
| `201` | Created | Recurso creado |
| `202` | Accepted | Comando aceptado (relay) |
| `204` | No Content | Eliminación exitosa |
| `400` | Bad Request | Datos inválidos |
| `401` | Unauthorized | Token inválido/faltante |
| `403` | Forbidden | Sin permisos |
| `404` | Not Found | Recurso no existe |
| `409` | Conflict | MAC duplicada, etc. |
| `422` | Validation Error | Errores de validación |
| `500` | Server Error | Error interno |

---

## 🔧 Tipos de Dispositivos Disponibles

| ID | Nombre | Descripción | Comandos |
|----|--------|-------------|-----------|
| `5` | `NODO_CONTROL_PZEM` | Control con relé | ⚡ Relay ON/OFF |
| `6` | `NODO_SENSADO_RPI` | Sensado Raspberry Pi | 📊 Solo lecturas |

---

## 🎭 Roles del Sistema

| ID | Nombre | Permisos |
|----|--------|----------|
| `1` | `ADMIN` | ✅ Acceso completo |
| `2` | `USER` | 📖 Lectura + gestión propia |

---

## 🚦 Estados de Notificaciones

| Tipo | Color | Uso |
|------|-------|-----|
| `INFO` | 🔵 Azul | Información general |
| `WARNING` | 🟡 Amarillo | Advertencias |
| `ERROR` | 🔴 Rojo | Errores críticos |
| `SUCCESS` | 🟢 Verde | Operaciones exitosas |

---

## 🔗 URLs de Swagger/OpenAPI

- **Documentación Interactiva**: `http://127.0.0.1:8000/docs`
- **Esquema OpenAPI**: `http://127.0.0.1:8000/openapi.json`

---

## 📱 Ejemplos de Requests Comunes

### Login
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Crear Dispositivo
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/devices/" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi ESP32",
    "mac_address": "AA:BB:CC:DD:EE:FF",
    "device_type_id": 5,
    "location_id": 1
  }'
```

### Controlar Relé
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/devices/AA:BB:CC:DD:EE:FF/command/relay" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"action": "ON"}'
```

### Obtener Lecturas
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/lecturas-pzem/?device_mac=AA:BB:CC:DD:EE:FF&limit=10" \
  -H "Authorization: Bearer {token}"
```

---

## 💡 Tips para Desarrolladores Frontend

1. **Siempre manejar errores 401**: Token expirado → redirigir a login
2. **Validar device_type_id**: Solo type 5 puede usar comando relay
3. **MAC formato**: Usar formato `XX:XX:XX:XX:XX:XX` (mayúsculas)
4. **Polling para lecturas**: Consultar lecturas cada 30-60 segundos
5. **Notificaciones en tiempo real**: Considerar WebSockets para el futuro
6. **Caché local**: Guardar ubicaciones y tipos para evitar requests repetidos

Esta referencia rápida proporciona toda la información esencial que un desarrollador frontend necesita para integrar con la API Voltio de manera eficiente.
