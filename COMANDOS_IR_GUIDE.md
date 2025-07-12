# 📡 Módulo ComandosIR - Guía de Uso

## 🎯 Descripción

El módulo **ComandosIR** gestiona comandos de infrarrojo asociados a sensores, permitiendo el control remoto de dispositivos mediante códigos IR.

## 🏗️ Estructura de Datos

```json
{
  "id_comando": 1,
  "id_sensor": 100,
  "nombre": "Encender LED",
  "descripcion": "Comando para encender el LED principal",
  "comando": "LED_ON_IR_CODE_12345"
}
```

## 🔧 Endpoints Disponibles

### 1. Listar todos los comandos IR
```http
GET /api/v1/comandos-ir/
```
**Respuesta**: Lista de todos los comandos IR

### 2. Obtener comando IR por ID
```http
GET /api/v1/comandos-ir/{id_comando}
```
**Respuesta**: Comando IR específico

### 3. Obtener comandos IR por sensor
```http
GET /api/v1/comandos-ir/sensor/{id_sensor}
```
**Respuesta**: Lista de comandos IR para un sensor específico

### 4. Crear nuevo comando IR
```http
POST /api/v1/comandos-ir/
```
**Body**:
```json
{
  "id_sensor": 100,
  "nombre": "Apagar LED",
  "descripcion": "Comando para apagar el LED principal",
  "comando": "LED_OFF_IR_CODE_54321"
}
```

### 5. Actualizar comando IR
```http
PUT /api/v1/comandos-ir/{id_comando}
```
**Body**:
```json
{
  "nombre": "Apagar LED Completamente",
  "descripcion": "Comando para apagar completamente el LED",
  "comando": "LED_OFF_COMPLETE_IR_CODE_99999"
}
```

### 6. Eliminar comando IR
```http
DELETE /api/v1/comandos-ir/{id_comando}
```

## 🔐 Seguridad

- **Lectura** (`GET`): Requiere autenticación
- **Creación/Actualización** (`POST`/`PUT`): Requiere rol Admin o Moderador
- **Eliminación** (`DELETE`): Requiere rol Admin

## ✅ Validaciones

### Reglas de Negocio
- **Nombre**: Mínimo 3 caracteres
- **Comando**: No puede estar vacío
- **ID Sensor**: Debe ser un número entero positivo
- **Descripción**: Campo requerido

### Validaciones de Base de Datos
- **ID Comando**: Autoincremental, clave primaria
- **ID Sensor**: Índice para búsquedas optimizadas
- **Nombre**: Índice para búsquedas rápidas

## 🚀 Casos de Uso Comunes

### 1. Configurar comandos para un sensor
```bash
# Crear comando de encendido
curl -X POST "http://localhost:8000/api/v1/comandos-ir/" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "id_sensor": 100,
    "nombre": "Encender",
    "descripcion": "Encender dispositivo",
    "comando": "PWR_ON_12345"
  }'

# Crear comando de apagado
curl -X POST "http://localhost:8000/api/v1/comandos-ir/" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "id_sensor": 100,
    "nombre": "Apagar",
    "descripcion": "Apagar dispositivo",
    "comando": "PWR_OFF_12345"
  }'
```

### 2. Obtener todos los comandos de un sensor
```bash
curl -X GET "http://localhost:8000/api/v1/comandos-ir/sensor/100" \
  -H "Authorization: Bearer {token}"
```

### 3. Actualizar un comando existente
```bash
curl -X PUT "http://localhost:8000/api/v1/comandos-ir/1" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Encender Completo",
    "comando": "PWR_ON_FULL_67890"
  }'
```

## 🎨 Ejemplos de Comandos IR

### Comandos de Audio/Video
```json
{
  "id_sensor": 100,
  "nombre": "Subir Volumen",
  "descripcion": "Aumentar el volumen del dispositivo",
  "comando": "VOL_UP_IR_A1B2C3"
}
```

### Comandos de Iluminación
```json
{
  "id_sensor": 200,
  "nombre": "Atenuar Luz",
  "descripcion": "Reducir intensidad de la luz",
  "comando": "LIGHT_DIM_IR_D4E5F6"
}
```

### Comandos de Climatización
```json
{
  "id_sensor": 300,
  "nombre": "Temperatura +",
  "descripcion": "Aumentar temperatura del aire acondicionado",
  "comando": "AC_TEMP_UP_IR_G7H8I9"
}
```

## 📊 Estructura de Respuesta de Error

```json
{
  "detail": "Comando IR con ID 999 no encontrado"
}
```

## 🔍 Filtros y Búsquedas

El módulo incluye funcionalidad específica para:
- Buscar comandos por sensor
- Filtrar por nombre (implementación futura)
- Agrupar por tipo de comando (implementación futura)

## 🌟 Características Avanzadas

### Preparado para Ejecución
La estructura está preparada para implementar:
- Ejecución de comandos IR en tiempo real
- Historial de comandos ejecutados
- Programación de comandos
- Macros de comandos múltiples

### Integración con Sensores
- Relación directa con el módulo Sensores (cuando se implemente)
- Validación de existencia de sensores
- Agrupación automática por sensor
