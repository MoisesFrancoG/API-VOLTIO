# 🔧 API VOLTIO - Esquemas de Datos Técnicos

## 📊 Esquemas de Request/Response

### 👥 Usuarios (Users)

#### UserCreate
```json
{
  "username": "string",              // 1-100 caracteres
  "email": "user@example.com",       // Email válido, max 100 caracteres
  "password": "string",              // Mínimo 6 caracteres, max 255
  "role_id": 2                       // Default: 2 (USER), 1 = ADMIN
}
```

#### UserResponse
```json
{
  "id": 1,
  "username": "string",
  "email": "user@example.com",
  "role_id": 2,
  "created_at": "2025-01-20T10:00:00Z"
}
```

#### UserLogin
```json
{
  "email": "user@example.com",
  "password": "string"
}
```

#### UserUpdate
```json
{
  "username": "string",              // Opcional
  "email": "user@example.com",       // Opcional
  "role_id": 2                       // Opcional
}
```

#### UserUpdatePassword
```json
{
  "current_password": "string",
  "new_password": "string"           // Mínimo 6 caracteres
}
```

#### TokenResponse
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

---

### 🏷️ Roles

#### RoleCreate
```json
{
  "name": "string",                  // Nombre del rol
  "description": "string"            // Descripción opcional
}
```

#### RoleResponse
```json
{
  "id": 1,
  "name": "ADMIN",
  "description": "Administrator role"
}
```

#### RoleUpdate
```json
{
  "name": "string",                  // Opcional
  "description": "string"            // Opcional
}
```

---

### 📍 Ubicaciones (Locations)

#### LocationCreate
```json
{
  "name": "string",                  // Nombre de la ubicación
  "description": "string"            // Descripción opcional
}
```

#### LocationResponse
```json
{
  "id": 1,
  "name": "Oficina Principal",
  "description": "Ubicación principal del edificio"
}
```

#### LocationUpdate
```json
{
  "name": "string",                  // Opcional
  "description": "string"            // Opcional
}
```

---

### 🔧 Tipos de Dispositivos (Device Types)

#### DeviceTypeCreate
```json
{
  "type_name": "string",             // Nombre del tipo
  "description": "string"            // Descripción opcional
}
```

#### DeviceTypeResponse
```json
{
  "id": 5,
  "type_name": "NODO_CONTROL_PZEM",
  "description": "Dispositivo de control con relé"
}
```

#### DeviceTypeUpdate
```json
{
  "type_name": "string",             // Opcional
  "description": "string"            // Opcional
}
```

---

### 🔌 Dispositivos (Devices)

#### DeviceCreate
```json
{
  "name": "string",                  // Nombre del dispositivo
  "mac_address": "AA:BB:CC:DD:EE:FF", // MAC único, formato XX:XX:XX:XX:XX:XX
  "device_type_id": 5,               // ID del tipo de dispositivo
  "location_id": 1,                  // ID de la ubicación
  "description": "string"            // Descripción opcional
}
```

#### DeviceResponse
```json
{
  "id": 1,
  "name": "Mi Dispositivo",
  "mac_address": "AA:BB:CC:DD:EE:FF",
  "device_type_id": 5,
  "location_id": 1,
  "user_id": 1,                      // ID del propietario
  "description": "Descripción del dispositivo",
  "created_at": "2025-01-20T10:00:00Z",
  "updated_at": "2025-01-20T10:00:00Z"
}
```

#### DeviceUpdate
```json
{
  "name": "string",                  // Opcional
  "description": "string",           // Opcional
  "location_id": 1                   // Opcional
}
```

---

### ⚡ Comando de Relé

#### RelayCommandRequest
```json
{
  "action": "ON"                     // "ON" | "OFF"
}
```

#### RelayCommandResponse
```json
{
  "status": "Comando de relé enviado al dispositivo",
  "device_mac": "AA:BB:CC:DD:EE:FF",
  "action_sent": "ON"
}
```

---

### 📡 Comandos IR (Device Commands)

#### DeviceCommandCreate
```json
{
  "device_capability_instance_id": 1, // ID de la instancia
  "device_name": "TV Samsung",         // Nombre del dispositivo IR
  "command_name": "POWER",             // Nombre del comando
  "ir_code": "FF00FF00FF00FF00",       // Código IR en hexadecimal
  "description": "Comando de encendido" // Descripción opcional
}
```

#### DeviceCommandResponse
```json
{
  "id": 1,
  "device_capability_instance_id": 1,
  "device_name": "TV Samsung",
  "command_name": "POWER",
  "ir_code": "FF00FF00FF00FF00",
  "description": "Comando de encendido",
  "created_at": "2025-01-20T10:00:00Z"
}
```

#### DeviceCommandUpdate
```json
{
  "device_name": "string",           // Opcional
  "command_name": "string",          // Opcional
  "ir_code": "string",               // Opcional
  "description": "string"            // Opcional
}
```

---

### 📊 Lecturas PZEM

#### PzemReadingResponse
```json
{
  "time": "2025-01-20T10:00:00Z",    // Timestamp en UTC
  "device_mac": "AA:BB:CC:DD:EE:FF", // MAC del dispositivo
  "voltage": 220.5,                  // Voltaje en V
  "current": 1.2,                    // Corriente en A
  "power": 264.6,                    // Potencia en W
  "energy": 1000.0,                  // Energía en Wh
  "frequency": 60.0,                 // Frecuencia en Hz
  "power_factor": 0.95               // Factor de potencia (0-1)
}
```

#### Query Parameters para Lecturas
```
device_mac: string                   // MAC del dispositivo (requerido)
start_time: string                   // ISO datetime (opcional)
end_time: string                     // ISO datetime (opcional)
limit: integer                       // Max registros (default: 1000)
```

---

### 🔔 Notificaciones

#### NotificationCreate
```json
{
  "title": "string",                 // Título de la notificación
  "message": "string",               // Mensaje de la notificación
  "type": "INFO",                    // "INFO" | "WARNING" | "ERROR" | "SUCCESS"
  "user_id": 1                       // ID del usuario destinatario
}
```

#### NotificationResponse
```json
{
  "id": 1,
  "title": "Título de la notificación",
  "message": "Mensaje de la notificación",
  "type": "INFO",
  "user_id": 1,
  "is_read": false,
  "created_at": "2025-01-20T10:00:00Z",
  "read_at": null                    // Timestamp cuando se marcó como leída
}
```

#### NotificationUpdate
```json
{
  "is_read": true                    // Marcar como leída/no leída
}
```

---

### 🔔 Servicio de Notificaciones

#### ServiceNotificationRequest
```json
{
  "device_mac": "AA:BB:CC:DD:EE:FF", // MAC del dispositivo
  "message": "string",               // Mensaje de servicio
  "severity": "INFO"                 // "INFO" | "WARNING" | "ERROR"
}
```

#### ManualNotificationRequest
```json
{
  "user_ids": [1, 2, 3],            // Lista de IDs de usuarios
  "title": "string",                 // Título
  "message": "string",               // Mensaje
  "type": "INFO"                     // Tipo de notificación
}
```

#### BulkReadRequest
```json
{
  "notification_ids": [1, 2, 3, 4]  // Lista de IDs a marcar como leídas
}
```

---

## 🚨 Esquemas de Error

### ErrorResponse
```json
{
  "detail": "Descripción del error"
}
```

### ValidationError (422)
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "email"],
      "msg": "Field required",
      "input": {...}
    }
  ]
}
```

### AuthenticationError (401)
```json
{
  "detail": "Could not validate credentials"
}
```

### PermissionError (403)
```json
{
  "detail": "Sin permisos. Roles requeridos: [1]"
}
```

### NotFoundError (404)
```json
{
  "detail": "Dispositivo no encontrado"
}
```

### ConflictError (409)
```json
{
  "detail": "Ya existe un dispositivo con esta MAC"
}
```

---

## 📋 Validaciones de Campos

### Campos de Usuario
- **username**: 1-100 caracteres, alfanumérico y guiones permitidos
- **email**: Formato de email válido, max 100 caracteres, único
- **password**: Mínimo 6 caracteres, max 255
- **role_id**: Entero positivo (1=ADMIN, 2=USER)

### Campos de Dispositivo
- **name**: String no vacío
- **mac_address**: Formato XX:XX:XX:XX:XX:XX, único en el sistema
- **device_type_id**: Debe existir en device_types
- **location_id**: Debe existir en locations
- **description**: String opcional

### Campos de Comando IR
- **device_name**: String no vacío
- **command_name**: String no vacío
- **ir_code**: String hexadecimal válido
- **device_capability_instance_id**: Entero positivo

### Campos de Relé
- **action**: Exactamente "ON" o "OFF" (case sensitive)

---

## 🔗 Relaciones de Datos

```
Users (1) ──→ (N) Devices
Locations (1) ──→ (N) Devices
DeviceTypes (1) ──→ (N) Devices
Users (1) ──→ (N) Notifications
Roles (1) ──→ (N) Users
```

### Restricciones de Integridad
- No se puede eliminar una ubicación con dispositivos asociados
- No se puede eliminar un tipo de dispositivo con dispositivos asociados
- No se puede eliminar un usuario con dispositivos asociados
- Solo el propietario puede modificar/eliminar sus dispositivos
- Solo admin puede modificar datos maestros (roles, ubicaciones, tipos)

---

## 🔄 Estados de Respuesta HTTP

| Método | Éxito | Recurso Creado | Sin Contenido |
|--------|-------|----------------|---------------|
| GET    | 200   | -              | -             |
| POST   | 200   | 201            | -             |
| PUT    | 200   | -              | -             |
| DELETE | 200   | -              | 204           |

### Códigos de Error Específicos por Endpoint

#### Dispositivos
- **POST /devices/**: 409 si MAC duplicada
- **PUT /devices/{id}**: 403 si no es propietario
- **DELETE /devices/{id}**: 403 si no es propietario

#### Comando de Relé
- **POST /devices/{mac}/command/relay**: 
  - 409 si dispositivo no es NODO_CONTROL_PZEM
  - 403 si no es propietario
  - 400 si action inválida

#### Datos Maestros (Admin only)
- **POST|PUT|DELETE** en roles, ubicaciones, device-types: 403 si no es admin

---

Esta documentación técnica complementa la documentación principal y proporciona todos los detalles necesarios para implementar la integración frontend correctamente.
