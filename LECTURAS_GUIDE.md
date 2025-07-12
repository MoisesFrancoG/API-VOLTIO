# Guía del Módulo de Lecturas

## Descripción General

El módulo de Lecturas gestiona las mediciones de sensores en el sistema Voltio. Permite crear, consultar, actualizar y eliminar lecturas, así como realizar análisis estadísticos y de tendencias.

## Estructura del Módulo

```
src/Lecturas/
├── domain/
│   ├── entities.py          # Entidad de dominio Lectura
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

## Endpoints Disponibles

### 1. Crear Lectura
- **POST** `/api/v1/lecturas/`
- **Cuerpo**: `LecturaCreate`
```json
{
  "id_sensor": 1,
  "valor": 25.5,
  "unidad": "°C",
  "fecha_hora": "2024-01-01T12:00:00"
}
```

### 2. Obtener Lectura por ID
- **GET** `/api/v1/lecturas/{id_lectura}`
- **Respuesta**: `LecturaResponse`

### 3. Obtener Todas las Lecturas
- **GET** `/api/v1/lecturas/`
- **Respuesta**: `List[LecturaResponse]`

### 4. Obtener Lecturas por Sensor
- **GET** `/api/v1/lecturas/sensor/{id_sensor}`
- **Respuesta**: `List[LecturaResponse]`

### 5. Obtener Últimas Lecturas por Sensor
- **GET** `/api/v1/lecturas/sensor/{id_sensor}/ultimas?limite=10`
- **Parámetros**: `limite` (1-100)
- **Respuesta**: `List[LecturaResponse]`

### 6. Obtener Lecturas por Rango de Fechas
- **GET** `/api/v1/lecturas/rango-fechas/?fecha_inicio=2024-01-01T00:00:00&fecha_fin=2024-01-02T00:00:00`
- **Parámetros**: `fecha_inicio`, `fecha_fin` (formato ISO)
- **Respuesta**: `List[LecturaResponse]`

### 7. Obtener Lecturas por Sensor y Fechas
- **GET** `/api/v1/lecturas/sensor/{id_sensor}/rango-fechas?fecha_inicio=2024-01-01T00:00:00&fecha_fin=2024-01-02T00:00:00`
- **Respuesta**: `List[LecturaResponse]`

### 8. Obtener Lecturas Críticas
- **GET** `/api/v1/lecturas/criticas/?limite_superior=100&limite_inferior=0`
- **Parámetros**: `limite_superior`, `limite_inferior`
- **Respuesta**: `List[LecturaResponse]`

### 9. Obtener Estadísticas por Sensor
- **GET** `/api/v1/lecturas/sensor/{id_sensor}/estadisticas`
- **Respuesta**:
```json
{
  "id_sensor": 1,
  "total_lecturas": 150,
  "valor_promedio": 25.3,
  "valor_minimo": 20.1,
  "valor_maximo": 30.5
}
```

### 10. Análisis de Tendencia por Sensor
- **GET** `/api/v1/lecturas/sensor/{id_sensor}/tendencia?limite_lecturas=100`
- **Respuesta**:
```json
{
  "id_sensor": 1,
  "tendencia": "creciente",
  "porcentaje_cambio": 2.5,
  "valor_inicial": 24.5,
  "valor_final": 25.1,
  "total_lecturas": 100
}
```

### 11. Contar Lecturas por Sensor
- **GET** `/api/v1/lecturas/sensor/{id_sensor}/contar`
- **Respuesta**:
```json
{
  "id_sensor": 1,
  "total_lecturas": 150
}
```

### 12. Actualizar Lectura
- **PUT** `/api/v1/lecturas/{id_lectura}`
- **Cuerpo**: `LecturaUpdate`
```json
{
  "valor": 26.0,
  "unidad": "°C"
}
```

### 13. Eliminar Lectura
- **DELETE** `/api/v1/lecturas/{id_lectura}`
- **Respuesta**: `{"mensaje": "Lectura eliminada exitosamente"}`

## Esquemas de Datos

### LecturaCreate
```python
{
  "id_sensor": int,        # ID del sensor (>0)
  "valor": float,          # Valor de la lectura (>=0)
  "unidad": str,           # Unidad de medida (válida)
  "fecha_hora": datetime   # Fecha y hora (opcional)
}
```

### LecturaUpdate
```python
{
  "id_sensor": int,        # ID del sensor (opcional)
  "valor": float,          # Valor de la lectura (opcional)
  "unidad": str           # Unidad de medida (opcional)
}
```

### LecturaResponse
```python
{
  "id_lectura": int,       # ID único de la lectura
  "id_sensor": int,        # ID del sensor
  "valor": float,          # Valor de la lectura
  "unidad": str,           # Unidad de medida
  "fecha_hora": datetime   # Fecha y hora de la lectura
}
```

## Unidades de Medida Válidas

- `°C` - Celsius
- `°F` - Fahrenheit
- `V` - Voltios
- `A` - Amperios
- `W` - Vatios
- `kW` - Kilovatios
- `kWh` - Kilovatios-hora
- `%` - Porcentaje
- `ppm` - Partes por millón
- `bar` - Bares
- `Pa` - Pascales
- `m/s` - Metros por segundo
- `Hz` - Hercios

## Validaciones

### Validaciones de Dominio
- Los valores no pueden ser negativos
- Las unidades deben ser válidas
- Los IDs de sensor deben ser positivos
- Las fechas de inicio deben ser anteriores a las de fin

### Validaciones de Esquema
- Campos obligatorios validados
- Tipos de datos correctos
- Rangos de valores apropiados
- Formato de fecha válido

## Reglas de Negocio

### Análisis de Criticidad
- Una lectura es crítica si está fuera de los límites establecidos
- Límites configurables por consulta
- Útil para alertas y monitoreo

### Análisis de Tendencia
- Compara primera y última lectura en un conjunto
- Clasifica como: estable, creciente, decreciente
- Calcula porcentaje de cambio
- Requiere al menos 2 lecturas

### Conversión de Temperatura
- Soporte para conversión entre °C y °F
- Implementado en la entidad de dominio
- Validaciones de unidades compatibles

## Casos de Uso Principales

### 1. Registro de Lectura
```python
# Crear una nueva lectura
lectura = await use_cases.crear_lectura(LecturaCreate(
    id_sensor=1,
    valor=25.5,
    unidad="°C"
))
```

### 2. Consulta de Historial
```python
# Obtener historial de un sensor
lecturas = await use_cases.obtener_lecturas_por_sensor(1)
```

### 3. Monitoreo de Anomalías
```python
# Detectar lecturas críticas
criticas = await use_cases.obtener_lecturas_criticas(
    limite_superior=100.0,
    limite_inferior=0.0
)
```

### 4. Análisis Estadístico
```python
# Obtener estadísticas completas
stats = await use_cases.obtener_estadisticas_sensor(1)
```

## Ejemplos de Uso

### Ejemplo 1: Crear y Consultar Lecturas
```bash
# Crear lectura
curl -X POST "http://localhost:8000/api/v1/lecturas/" \
  -H "Content-Type: application/json" \
  -d '{"id_sensor": 1, "valor": 25.5, "unidad": "°C"}'

# Obtener lecturas del sensor
curl "http://localhost:8000/api/v1/lecturas/sensor/1"
```

### Ejemplo 2: Análisis de Tendencias
```bash
# Analizar tendencia
curl "http://localhost:8000/api/v1/lecturas/sensor/1/tendencia?limite_lecturas=50"
```

### Ejemplo 3: Monitoreo de Valores Críticos
```bash
# Obtener lecturas críticas
curl "http://localhost:8000/api/v1/lecturas/criticas/?limite_superior=100&limite_inferior=0"
```

## Manejo de Errores

### Códigos de Estado HTTP
- `200` - Operación exitosa
- `400` - Error de validación
- `404` - Recurso no encontrado
- `500` - Error interno del servidor

### Errores Comunes
- `ValueError` - Datos inválidos
- `ValidationError` - Esquema incorrecto
- `NotFoundError` - Recurso no existe

## Integración con Otros Módulos

### Relación con Sensores
- Cada lectura está asociada a un sensor
- Validación de existencia del sensor (futuro)
- Navegación bidireccional sensor-lecturas

### Relación con Alertas
- Las lecturas críticas pueden generar alertas
- Integración con sistema de notificaciones
- Análisis de patrones anómalos

## Consideraciones de Rendimiento

### Indexación
- Índices en `id_sensor` para consultas rápidas
- Índices en `fecha_hora` para rangos temporales
- Índice primario en `id_lectura`

### Optimizaciones
- Consultas limitadas por defecto
- Agregaciones eficientes para estadísticas
- Paginación recomendada para grandes conjuntos

## Próximas Funcionalidades

### Agregaciones Avanzadas
- Promedios por intervalos de tiempo
- Máximos y mínimos por período
- Análisis de variabilidad

### Filtros Adicionales
- Filtros por tipo de sensor
- Filtros por ubicación
- Filtros por rangos de valores

### Notificaciones
- Alertas automáticas por valores críticos
- Notificaciones de tendencias anómalas
- Integración con sistema de alertas

## Comandos de Prueba

```bash
# Ejecutar pruebas del módulo
python test_lecturas.py

# Verificar funcionalidad específica
python -c "
import asyncio
from test_lecturas import test_lecturas_crud
asyncio.run(test_lecturas_crud())
"
```

## Notas Importantes

1. **Validación de Sensores**: Actualmente no se valida la existencia del sensor, se asume que existe.
2. **Fechas**: Si no se proporciona fecha_hora, se usa la fecha/hora actual.
3. **Unidades**: Las unidades están predefinidas y no son extensibles sin modificar el código.
4. **Eliminación**: La eliminación es física, no lógica (se pierde el dato).
5. **Rendimiento**: Para consultas masivas, considerar implementar paginación.

Este módulo proporciona una base sólida para la gestión de lecturas de sensores con capacidades avanzadas de análisis y monitoreo.
