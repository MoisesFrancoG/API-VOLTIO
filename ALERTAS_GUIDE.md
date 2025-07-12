# 🚨 Módulo Alertas - Guía de Uso

## 🎯 Descripción

El módulo **Alertas** gestiona el sistema de notificaciones del sistema Voltio, permitiendo la creación, consulta y gestión de alertas basadas en lecturas de sensores.

## 🏗️ Estructura de Datos

```json
{
  "id_alerta": 1,
  "id_lectura": 100,
  "tipo_alerta": "CRITICA",
  "descripcion": "Temperatura crítica detectada: 85°C",
  "fecha_hora": "2025-07-12T10:30:00Z"
}
```

## 📋 Tipos de Alertas Predefinidos

- **CRITICA**: Situaciones que requieren atención inmediata
- **ADVERTENCIA**: Situaciones que requieren monitoreo
- **INFO**: Información general del sistema
- **ERROR**: Errores técnicos del sistema
- **MANTENIMIENTO**: Alertas relacionadas con mantenimiento

## 🔧 Endpoints Disponibles

### 1. Listar todas las alertas
```http
GET /api/v1/alertas/
```
**Respuesta**: Lista de todas las alertas ordenadas por fecha descendente

### 2. Obtener alerta por ID
```http
GET /api/v1/alertas/{id_alerta}
```
**Respuesta**: Alerta específica

### 3. Obtener alertas críticas
```http
GET /api/v1/alertas/criticas
```
**Respuesta**: Lista de alertas con tipo "CRITICA"

### 4. Obtener alertas recientes
```http
GET /api/v1/alertas/recientes?horas=24
```
**Parámetros**:
- `horas`: Número de horas hacia atrás (1-168, default: 24)

### 5. Generar reporte de alertas críticas
```http
GET /api/v1/alertas/reporte-criticas
```
**Respuesta**: Reporte completo con estadísticas

### 6. Obtener alertas por tipo
```http
GET /api/v1/alertas/tipo/{tipo_alerta}
```
**Ejemplo**: `/api/v1/alertas/tipo/ADVERTENCIA`

### 7. Obtener alertas por lectura
```http
GET /api/v1/alertas/lectura/{id_lectura}
```
**Respuesta**: Alertas asociadas a una lectura específica

### 8. Crear nueva alerta
```http
POST /api/v1/alertas/
```
**Body**:
```json
{
  "id_lectura": 100,
  "tipo_alerta": "CRITICA",
  "descripcion": "Temperatura crítica detectada: 85°C"
}
```

### 9. Actualizar alerta
```http
PUT /api/v1/alertas/{id_alerta}
```
**Body**:
```json
{
  "tipo_alerta": "ADVERTENCIA",
  "descripcion": "Temperatura normalizada: 25°C"
}
```

### 10. Eliminar alerta
```http
DELETE /api/v1/alertas/{id_alerta}
```

## 🔐 Seguridad

- **Lectura** (`GET`): Requiere autenticación
- **Creación/Actualización** (`POST`/`PUT`): Requiere rol Admin o Moderador
- **Eliminación** (`DELETE`): Requiere rol Admin

## ✅ Validaciones

### Reglas de Negocio
- **Descripción**: Mínimo 5 caracteres
- **Tipo Alerta**: Debe ser uno de los tipos predefinidos
- **ID Lectura**: Debe ser un número entero positivo
- **Fecha/Hora**: Se asigna automáticamente si no se proporciona

### Validaciones de Base de Datos
- **ID Alerta**: Autoincremental, clave primaria
- **ID Lectura**: Índice para búsquedas optimizadas
- **Tipo Alerta**: Índice para filtros por tipo
- **Fecha/Hora**: Índice para consultas temporales

## 🚀 Casos de Uso Comunes

### 1. Monitoreo de Alertas Críticas
```bash
# Obtener todas las alertas críticas
curl -X GET "http://localhost:8000/api/v1/alertas/criticas" \
  -H "Authorization: Bearer {token}"

# Generar reporte de alertas críticas
curl -X GET "http://localhost:8000/api/v1/alertas/reporte-criticas" \
  -H "Authorization: Bearer {token}"
```

### 2. Consulta de Alertas Recientes
```bash
# Alertas de las últimas 12 horas
curl -X GET "http://localhost:8000/api/v1/alertas/recientes?horas=12" \
  -H "Authorization: Bearer {token}"

# Alertas de la última semana
curl -X GET "http://localhost:8000/api/v1/alertas/recientes?horas=168" \
  -H "Authorization: Bearer {token}"
```

### 3. Crear Alertas Automáticas
```bash
# Crear alerta crítica
curl -X POST "http://localhost:8000/api/v1/alertas/" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "id_lectura": 100,
    "tipo_alerta": "CRITICA",
    "descripcion": "Temperatura crítica detectada: 85°C en sensor de sala principal"
  }'
```

### 4. Filtrar Alertas por Tipo
```bash
# Alertas de mantenimiento
curl -X GET "http://localhost:8000/api/v1/alertas/tipo/MANTENIMIENTO" \
  -H "Authorization: Bearer {token}"

# Alertas de error
curl -X GET "http://localhost:8000/api/v1/alertas/tipo/ERROR" \
  -H "Authorization: Bearer {token}"
```

## 📊 Estructura de Reporte de Alertas Críticas

```json
{
  "total_criticas": 15,
  "criticas_recientes_24h": 3,
  "alertas_criticas": [
    {
      "id_alerta": 1,
      "id_lectura": 100,
      "tipo_alerta": "CRITICA",
      "descripcion": "Temperatura crítica: 85°C",
      "fecha_hora": "2025-07-12T10:30:00Z"
    }
  ],
  "alertas_recientes": [
    {
      "id_alerta": 15,
      "id_lectura": 200,
      "tipo_alerta": "CRITICA",
      "descripcion": "Humedad crítica: 95%",
      "fecha_hora": "2025-07-12T14:45:00Z"
    }
  ]
}
```

## 🎨 Ejemplos de Alertas por Tipo

### Alertas Críticas
```json
{
  "id_lectura": 100,
  "tipo_alerta": "CRITICA",
  "descripcion": "Temperatura crítica detectada: 85°C - Riesgo de sobrecalentamiento"
}
```

### Alertas de Advertencia
```json
{
  "id_lectura": 101,
  "tipo_alerta": "ADVERTENCIA",
  "descripcion": "Humedad elevada: 80% - Monitorear condiciones ambientales"
}
```

### Alertas de Error
```json
{
  "id_lectura": 102,
  "tipo_alerta": "ERROR",
  "descripcion": "Fallo en comunicación con sensor - Verificar conexión"
}
```

### Alertas de Mantenimiento
```json
{
  "id_lectura": 103,
  "tipo_alerta": "MANTENIMIENTO",
  "descripcion": "Mantenimiento preventivo programado para sensor de temperatura"
}
```

### Alertas Informativas
```json
{
  "id_lectura": 104,
  "tipo_alerta": "INFO",
  "descripcion": "Sensor de humedad reiniciado correctamente"
}
```

## 🔍 Optimizaciones de Consulta

### Índices Implementados
- **Índice simple**: `id_alerta` (PRIMARY KEY)
- **Índice simple**: `id_lectura` (para búsquedas por lectura)
- **Índice simple**: `tipo_alerta` (para filtros por tipo)
- **Índice simple**: `fecha_hora` (para consultas temporales)
- **Índice compuesto**: `(tipo_alerta, fecha_hora)` (para alertas críticas recientes)
- **Índice compuesto**: `(id_lectura, fecha_hora)` (para histórico por lectura)

### Consultas Optimizadas
- Ordenamiento por fecha descendente por defecto
- Consultas con límite de tiempo para alertas recientes
- Filtros eficientes por tipo de alerta
- Agrupación por lectura optimizada

## 🌟 Características Avanzadas

### Preparado para Notificaciones
La estructura está preparada para implementar:
- Notificaciones en tiempo real (WebSockets)
- Emails automáticos para alertas críticas
- Webhooks para sistemas externos
- Integración con Slack/Teams
- SMS para alertas críticas

### Integración con Lecturas
- Relación directa con el módulo Lecturas (cuando se implemente)
- Validación de existencia de lecturas
- Agrupación automática por lectura
- Histórico de alertas por sensor

### Análisis y Reportes
- Estadísticas de alertas por tipo
- Tendencias temporales
- Alertas más frecuentes
- Tiempo de resolución (implementación futura)

## 🔧 Configuración Recomendada

### Políticas de Retención
- **Alertas INFO**: 30 días
- **Alertas ADVERTENCIA**: 90 días
- **Alertas ERROR**: 180 días
- **Alertas CRITICA**: 365 días
- **Alertas MANTENIMIENTO**: 180 días

### Umbrales Recomendados
- **Consultas recientes**: Máximo 168 horas (1 semana)
- **Alertas críticas**: Revisión cada 15 minutos
- **Reportes**: Generación diaria automática
- **Limpieza**: Proceso semanal de limpieza de alertas antiguas
