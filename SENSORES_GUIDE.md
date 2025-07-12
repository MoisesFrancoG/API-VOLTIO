# Guía del Módulo de Sensores

## Descripción General

El módulo de Sensores gestiona todos los dispositivos sensores del sistema Voltio. Permite crear, configurar, monitorear y administrar sensores con diferentes tipos, ubicaciones y usuarios asignados.

## Estructura del Módulo

```
src/Sensores/
├── domain/
│   ├── entities.py          # Entidad de dominio Sensor
│   └── schemas.py           # Esquemas Pydantic para validación
├── application/
│   ├── interfaces.py        # Interfaces abstractas
│   └── use_cases.py         # Casos de uso del negocio
└── infrastructure/
    ├── models.py           # Modelos SQLAlchemy
    ├── repositories.py     # Implementación de repositorios
    ├── routers.py          # Rutas FastAPI
    └── database.py         # Configuración de dependencias
```

## Campos del Sensor

Según el esquema de base de datos:

- **`id_sensor`** (serial/autoincrement) - Identificador único
- **`nombre`** (varchar) - Nombre descriptivo del sensor
- **`id_tipo_sensor`** (integer) - Relación con tabla `tipo_sensores`
- **`id_ubicacion`** (integer) - Relación con tabla `ubicaciones`
- **`id_usuario`** (integer) - Relación con tabla `usuarios`
- **`activo`** (boolean) - Estado activo/inactivo del sensor

## Endpoints Disponibles

### 1. Crear Sensor
- **POST** `/api/v1/sensores/`
- **Cuerpo**: `SensorCreate`
```json
{
  "nombre": "Sensor Temperatura Sala 1",
  "id_tipo_sensor": 1,
  "id_ubicacion": 1,
  "id_usuario": 1,
  "activo": true
}
```

### 2. Obtener Sensor por ID
- **GET** `/api/v1/sensores/{id_sensor}`
- **Respuesta**: `SensorResponse`

### 3. Obtener Todos los Sensores
- **GET** `/api/v1/sensores/`
- **Respuesta**: `List[SensorResponse]`

### 4. Obtener Sensores Activos
- **GET** `/api/v1/sensores/activos/`
- **Respuesta**: `List[SensorResponse]`

### 5. Obtener Sensores por Tipo
- **GET** `/api/v1/sensores/tipo/{id_tipo_sensor}`
- **Respuesta**: `List[SensorResponse]`

### 6. Obtener Sensores por Ubicación
- **GET** `/api/v1/sensores/ubicacion/{id_ubicacion}`
- **Respuesta**: `List[SensorResponse]`

### 7. Obtener Sensores por Usuario
- **GET** `/api/v1/sensores/usuario/{id_usuario}`
- **Respuesta**: `List[SensorResponse]`

### 8. Buscar Sensores por Nombre
- **GET** `/api/v1/sensores/buscar/?nombre={término}`
- **Parámetros**: `nombre` (mínimo 2 caracteres)
- **Respuesta**: `List[SensorResponse]`

### 9. Estadísticas por Tipo
- **GET** `/api/v1/sensores/tipo/{id_tipo_sensor}/estadisticas`
- **Respuesta**:
```json
{
  "id_tipo_sensor": 1,
  "total_sensores": 25,
  "sensores_activos": 22,
  "sensores_inactivos": 3,
  "porcentaje_activos": 88.0
}
```

### 10. Estadísticas por Ubicación
- **GET** `/api/v1/sensores/ubicacion/{id_ubicacion}/estadisticas`
- **Respuesta**: Similar a estadísticas por tipo

### 11. Estadísticas por Usuario
- **GET** `/api/v1/sensores/usuario/{id_usuario}/estadisticas`
- **Respuesta**: Similar a estadísticas por tipo

### 12. Validar Configuración
- **GET** `/api/v1/sensores/{id_sensor}/validar`
- **Respuesta**:
```json
{
  "id_sensor": 1,
  "configuracion_valida": true,
  "puede_generar_lecturas": true,
  "esta_activo": true,
  "validaciones": {
    "nombre_valido": true,
    "tipo_sensor_valido": true,
    "ubicacion_valida": true,
    "usuario_valido": true
  }
}
```

### 13. Actualizar Sensor
- **PUT** `/api/v1/sensores/{id_sensor}`
- **Cuerpo**: `SensorUpdate`
```json
{
  "nombre": "Nuevo Nombre",
  "id_tipo_sensor": 2,
  "activo": false
}
```

### 14. Cambiar Estado del Sensor
- **PATCH** `/api/v1/sensores/{id_sensor}/estado`
- **Cuerpo**: `SensorEstadoUpdate`
```json
{
  "activo": false
}
```

### 15. Eliminar Sensor
- **DELETE** `/api/v1/sensores/{id_sensor}`
- **Respuesta**: `{"mensaje": "Sensor eliminado exitosamente"}`

## Esquemas de Datos

### SensorCreate
```python
{
  "nombre": str,              # Nombre del sensor (3-100 caracteres)
  "id_tipo_sensor": int,      # ID del tipo de sensor (>0)
  "id_ubicacion": int,        # ID de la ubicación (>0)
  "id_usuario": int,          # ID del usuario (>0)
  "activo": bool              # Estado activo (por defecto: true)
}
```

### SensorUpdate
```python
{
  "nombre": str,              # Nombre del sensor (opcional)
  "id_tipo_sensor": int,      # ID del tipo de sensor (opcional)
  "id_ubicacion": int,        # ID de la ubicación (opcional)
  "id_usuario": int,          # ID del usuario (opcional)
  "activo": bool              # Estado activo (opcional)
}
```

### SensorResponse
```python
{
  "id_sensor": int,           # ID único del sensor
  "nombre": str,              # Nombre del sensor
  "id_tipo_sensor": int,      # ID del tipo de sensor
  "id_ubicacion": int,        # ID de la ubicación
  "id_usuario": int,          # ID del usuario
  "activo": bool              # Estado activo
}
```

### SensorEstadoUpdate
```python
{
  "activo": bool              # Estado activo del sensor
}
```

## Validaciones

### Validaciones de Dominio
- Nombres únicos entre sensores
- Nombres de al menos 3 caracteres
- IDs de tipo sensor, ubicación y usuario positivos
- Estados booleanos válidos

### Validaciones de Esquema
- Campos obligatorios validados
- Tipos de datos correctos
- Longitudes de cadenas apropiadas
- Rangos de valores numéricos

## Reglas de Negocio

### Gestión de Estados
- Un sensor puede estar activo o inactivo
- Solo los sensores activos pueden generar lecturas
- El cambio de estado es una operación específica

### Configuración Válida
- Un sensor debe tener nombre, tipo, ubicación y usuario asignados
- La configuración se valida antes de permitir la generación de lecturas
- Validaciones específicas para cada campo

### Nombres Únicos
- No pueden existir dos sensores con el mismo nombre
- Validación automática al crear y actualizar
- Exclusión del sensor actual al actualizar

## Casos de Uso Principales

### 1. Registro de Sensor
```python
# Crear un nuevo sensor
sensor = await use_cases.crear_sensor(SensorCreate(
    nombre="Sensor Temperatura Oficina",
    id_tipo_sensor=1,
    id_ubicacion=2,
    id_usuario=3,
    activo=True
))
```

### 2. Consulta por Filtros
```python
# Obtener sensores por tipo
sensores = await use_cases.obtener_sensores_por_tipo(1)

# Obtener sensores por ubicación
sensores = await use_cases.obtener_sensores_por_ubicacion(2)

# Obtener sensores activos
sensores = await use_cases.obtener_sensores_activos()
```

### 3. Gestión de Estados
```python
# Cambiar estado del sensor
sensor = await use_cases.cambiar_estado_sensor(1, False)

# Validar configuración
validacion = await use_cases.validar_configuracion_sensor(1)
```

### 4. Análisis Estadístico
```python
# Obtener estadísticas por tipo
stats = await use_cases.obtener_estadisticas_por_tipo(1)

# Obtener estadísticas por ubicación
stats = await use_cases.obtener_estadisticas_por_ubicacion(2)
```

## Ejemplos de Uso

### Ejemplo 1: Crear y Configurar Sensor
```bash
# Crear sensor
curl -X POST "http://localhost:8000/api/v1/sensores/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Sensor Humedad Laboratorio",
    "id_tipo_sensor": 2,
    "id_ubicacion": 1,
    "id_usuario": 1,
    "activo": true
  }'

# Validar configuración
curl "http://localhost:8000/api/v1/sensores/1/validar"
```

### Ejemplo 2: Gestión de Estados
```bash
# Desactivar sensor
curl -X PATCH "http://localhost:8000/api/v1/sensores/1/estado" \
  -H "Content-Type: application/json" \
  -d '{"activo": false}'

# Obtener solo sensores activos
curl "http://localhost:8000/api/v1/sensores/activos/"
```

### Ejemplo 3: Consultas Especializadas
```bash
# Buscar sensores por nombre
curl "http://localhost:8000/api/v1/sensores/buscar/?nombre=Temperatura"

# Estadísticas por tipo
curl "http://localhost:8000/api/v1/sensores/tipo/1/estadisticas"

# Sensores por ubicación
curl "http://localhost:8000/api/v1/sensores/ubicacion/1"
```

## Relaciones con Otros Módulos

### Dependencias
- **TipoSensores**: Cada sensor tiene un tipo asignado
- **Ubicaciones**: Cada sensor está en una ubicación específica
- **Usuarios**: Cada sensor pertenece a un usuario

### Módulos Relacionados
- **Lecturas**: Los sensores generan lecturas de mediciones
- **ComandosIR**: Los sensores pueden tener comandos IR asociados
- **Alertas**: Las lecturas de sensores pueden generar alertas

## Manejo de Errores

### Códigos de Estado HTTP
- `200` - Operación exitosa
- `400` - Error de validación
- `404` - Sensor no encontrado
- `500` - Error interno del servidor

### Errores Comunes
- `ValueError` - Datos inválidos o violaciones de reglas de negocio
- `ValidationError` - Esquema incorrecto
- `NotFoundError` - Sensor no existe
- `DuplicateError` - Nombre duplicado

## Optimizaciones de Base de Datos

### Indexación
- Índice único en `nombre` para consultas rápidas
- Índices en `id_tipo_sensor`, `id_ubicacion`, `id_usuario`
- Índice en `activo` para filtros de estado

### Consultas Optimizadas
- Filtros eficientes por tipo, ubicación y usuario
- Búsquedas por nombre con ILIKE
- Conteos agregados para estadísticas

## Próximas Funcionalidades

### Mejoras Operativas
- Paginación para consultas masivas
- Filtros combinados (ej: por tipo Y ubicación)
- Ordenamiento personalizable

### Funcionalidades Avanzadas
- Historial de cambios de estado
- Notificaciones de cambios de configuración
- Métricas de rendimiento por sensor

### Integración
- Validación de existencia de tipos, ubicaciones y usuarios
- Relaciones bidireccionales con otros módulos
- Sincronización con sistemas externos

## Comandos de Prueba

```bash
# Ejecutar pruebas del módulo
python test_sensores.py

# Verificar funcionalidad específica
python -c "
import asyncio
from test_sensores import test_sensores_crud
asyncio.run(test_sensores_crud())
"
```

## Notas Importantes

1. **Nombres Únicos**: Los nombres de sensores deben ser únicos en todo el sistema.
2. **Estados**: Solo los sensores activos pueden generar lecturas válidas.
3. **Validación**: Siempre validar la configuración antes de usar el sensor.
4. **Relaciones**: Actualmente no se valida la existencia de tipos, ubicaciones y usuarios.
5. **Eliminación**: La eliminación es física, no lógica.

Este módulo proporciona una gestión completa de sensores con capacidades avanzadas de administración, estadísticas y validación de configuración.
