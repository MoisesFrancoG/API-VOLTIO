# 🧪 API VOLTIO - Suite de Testing Automatizado

## 📚 Documentación y Scripts de Pruebas

Este repositorio incluye documentación completa y scripts automatizados para testing de la API VOLTIO.

## 📋 Archivos Creados

### 📖 Documentación

#### `DOCUMENTACION_COMPLETA_API.md`

- **Descripción:** Documentación completa de todos los endpoints de la API
- **Contenido:**
  - 📚 Información general y autenticación
  - 👥 Usuarios (Users) - 11 endpoints
  - 🏷️ Roles - 5 endpoints
  - 📍 Ubicaciones (Locations) - 5 endpoints
  - 🔧 Tipos de Dispositivos - 5 endpoints
  - 🔌 Dispositivos - 8+ endpoints
  - ⚡ Comando de Relé - 1 endpoint
  - 📡 Comandos IR - 6 endpoints
  - 📊 Lecturas PZEM - 3+ endpoints
  - 🔔 Notificaciones - 6+ endpoints
  - 🔔 Servicio de Notificaciones - 5 endpoints
  - 🧪 Endpoints de Prueba - 10+ endpoints
- **Total:** 65+ endpoints documentados
- **Incluye:** Ejemplos de request/response, códigos de estado, permisos requeridos

### 🤖 Scripts de Pruebas Automatizadas

#### `test_suite_completa.py` ⭐ **[PRINCIPAL]**

- **Descripción:** Suite completa de pruebas automatizadas
- **Características:**
  - ✅ Prueba todos los endpoints principales
  - 🔐 Autenticación automática (SuperAdmin + usuarios)
  - 📊 Generación de datos de prueba dinámicos
  - 📈 Reporte completo con estadísticas
  - 🏷️ Categorización de endpoints
  - 💾 Exportación de resultados en JSON
  - ⏱️ Medición de tiempos de ejecución

#### `test_quick.py` ⚡ **[RÁPIDO]**

- **Descripción:** Pruebas rápidas para verificaciones básicas
- **Características:**
  - 🚀 Ejecución rápida (< 30 segundos)
  - 🎯 Solo endpoints críticos
  - 💡 Ideal para CI/CD
  - 📋 Reporte simplificado
  - 🔍 Perfecto para debugging

#### `test_performance.py` 📈 **[RENDIMIENTO]**

- **Descripción:** Pruebas de carga y rendimiento
- **Características:**
  - ⚡ Pruebas de concurrencia
  - 📊 Medición de throughput
  - ⏱️ Análisis de tiempos de respuesta
  - 📈 Percentiles (P95, P99)
  - 🏆 Sistema de scoring
  - 💡 Recomendaciones de optimización

---

## 🚀 Cómo Usar los Scripts

### 📋 Prerrequisitos

```bash
# Instalar dependencias
pip install requests

# Verificar que la API esté corriendo
curl https://voltioapi.acstree.xyz/test/quick
```

### 🔧 Configuración

Cada script tiene configuración en la parte superior del archivo:

```python
# Cambiar ambiente
USE_PRODUCTION = True  # False para desarrollo local

# URLs
PROD_URL = "https://voltioapi.acstree.xyz"
DEV_URL = "http://127.0.0.1:8000"

# Credenciales (cambiar según necesidad)
CREDENTIALS = {
    "email": "superadmin@voltio.com",
    "password": "SuperAdmin123!"
}
```

---

## 📊 Scripts de Ejecución

### 1. 🧪 Suite Completa de Pruebas

```bash
# Ejecutar todas las pruebas
python test_suite_completa.py

# El script generará:
# - Reporte en consola con colores
# - Archivo JSON: api_test_report_prod_YYYYMMDD_HHMMSS.json
```

**Qué Prueba:**

- ✅ 20+ endpoints principales
- 🔐 Autenticación y autorización
- 📝 CRUD operations (Create, Read, Update, Delete)
- 🎯 Endpoints críticos para funcionamiento
- 🧪 Endpoints de sistema y monitoreo

**Tiempo Estimado:** 2-5 minutos

**Ejemplo de Salida:**

```
🚀 INICIANDO SUITE DE PRUEBAS AUTOMATIZADAS API VOLTIO
======================================================================
🌐 Ambiente: PRODUCCIÓN
🔗 Base URL: https://voltioapi.acstree.xyz
🕐 Tiempo: 2025-07-22 10:30:00
======================================================================

🧪 CATEGORÍA: SYSTEM
--------------------------------------------------
🔄 GET / - Root endpoint
   ✅ Status 200 (0.245s)
🔄 GET /test/quick - Quick health check
   ✅ Status 200 (0.123s)

📊 REPORTE FINAL DE PRUEBAS AUTOMATIZADAS
======================================================================
📈 ESTADÍSTICAS GENERALES:
   • Total de pruebas: 25
   • Exitosas: 23 ✅
   • Fallidas: 2 ❌
   • Tasa de éxito: 92.0%
   • Tiempo total: 45.67s

🎉 EVALUACIÓN: EXCELENTE - API funcionando perfectamente
======================================================================
```

### 2. ⚡ Pruebas Rápidas

```bash
# Ejecutar pruebas rápidas
python test_quick.py

# Archivo generado: quick_test_prod_YYYYMMDD_HHMMSS.json
```

**Qué Prueba:**

- 🏥 Health checks básicos
- 🔐 Autenticación SuperAdmin
- 📋 Endpoints críticos principales
- 🆕 Una prueba de creación

**Tiempo Estimado:** 10-30 segundos

**Ejemplo de Salida:**

```
🚀 API VOLTIO - Pruebas Rápidas v1.0

🚀 INICIANDO PRUEBAS RÁPIDAS API VOLTIO
============================================================
🌐 Ambiente: PRODUCCIÓN
🔗 URL: https://voltioapi.acstree.xyz

🧪 PRUEBAS DE SISTEMA
✅ GET / - Root endpoint: Status 200
✅ GET /test/quick - Health check rápido: Status 200

🔐 AUTENTICACIÓN
✅ Login SuperAdmin: SUCCESS

🔒 ENDPOINTS CRÍTICOS
✅ GET /users/me - Usuario actual: Status 200
✅ GET /devices/ - Lista dispositivos: Status 200

📊 RESUMEN DE PRUEBAS RÁPIDAS
============================================================
✅ Exitosas: 12
❌ Fallidas: 0
📊 Total: 12
📈 Tasa de éxito: 100.0%
⏱️ Tiempo: 8.45s

🎉 RESULTADO: API FUNCIONANDO PERFECTAMENTE
============================================================
```

### 3. 📈 Pruebas de Rendimiento

```bash
# Ejecutar pruebas de rendimiento
python test_performance.py

# Archivo generado: performance_report_prod_YYYYMMDD_HHMMSS.json
```

**Qué Prueba:**

- ⚡ Concurrencia (10 usuarios simultáneos)
- 📊 Carga sostenida (15 segundos)
- ⏱️ Tiempos de respuesta
- 🎯 Throughput (requests/segundo)

**Tiempo Estimado:** 1-2 minutos

**Ejemplo de Salida:**

```
⚡ INICIANDO PRUEBAS DE RENDIMIENTO API VOLTIO
======================================================================
🌐 Ambiente: PRODUCCIÓN
👥 Usuarios concurrentes: 10
⏱️ Duración de pruebas: 30s

🎯 PROBANDO: GET /users/me
🚀 Iniciando 10 peticiones concurrentes a /users/me
   📊 10/10 exitosas
   ⏱️ Tiempo promedio: 0.245s
   📈 P95: 0.421s

📊 REPORTE DE RENDIMIENTO
======================================================================
🎯 MÉTRICAS GENERALES:
   • Total peticiones: 156
   • Peticiones exitosas: 154
   • Tasa de éxito: 98.7%
   • Throughput: 12.45 req/s

⏱️ TIEMPOS DE RESPUESTA:
   • Promedio: 0.234s
   • P95: 0.456s
   • P99: 0.678s

🏆 EVALUACIÓN DE RENDIMIENTO: A MUY BUENO
   API con muy buen rendimiento
======================================================================
```

---

## 📊 Interpretación de Resultados

### ✅ Códigos de Exit

| Exit Code | Significado  | Condición           |
| --------- | ------------ | ------------------- |
| **0**     | Éxito        | Tasa de éxito ≥ 75% |
| **1**     | Fallo        | Tasa de éxito < 75% |
| **130**   | Interrumpido | Ctrl+C              |

### 📈 Evaluaciones

#### Suite Completa / Pruebas Rápidas:

- **🎉 EXCELENTE (90%+):** API funcionando perfectamente
- **✅ BUENO (75-89%):** API funcionando correctamente
- **⚠️ ACEPTABLE (50-74%):** Algunos problemas detectados
- **❌ CRÍTICO (<50%):** Múltiples fallas detectadas

#### Pruebas de Rendimiento:

- **🏆 A+ EXCELENTE (90+):** Rendimiento excepcional
- **🥇 A MUY BUENO (80-89):** Muy buen rendimiento
- **🥈 B BUENO (70-79):** Rendimiento aceptable
- **🥉 C REGULAR (60-69):** Requiere mejoras
- **❌ D CRÍTICO (<60):** Optimizaciones urgentes

---

## 🔧 Integración con CI/CD

### GitHub Actions

```yaml
name: API Testing
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install requests
      - name: Run quick tests
        run: python test_quick.py
      - name: Run full test suite
        run: python test_suite_completa.py
```

### Scripts de Monitoreo

```bash
#!/bin/bash
# Monitoreo automático cada 5 minutos
while true; do
    echo "$(date): Ejecutando health check..."
    python test_quick.py
    if [ $? -eq 0 ]; then
        echo "✅ API funcionando correctamente"
    else
        echo "❌ Problema detectado en API" | mail -s "API Alert" admin@voltio.com
    fi
    sleep 300
done
```

---

## 📁 Archivos de Resultado

### Formato JSON de Reportes

```json
{
  "timestamp": "2025-07-22T10:30:00",
  "environment": "production",
  "base_url": "https://voltioapi.acstree.xyz",
  "total_tests": 25,
  "successful_tests": 23,
  "failed_tests": 2,
  "success_rate": 92.0,
  "execution_time": 45.67,
  "evaluation": "EXCELLENT",
  "failed_tests_detail": [
    {
      "endpoint": "/lecturas-pzem/last_hour",
      "method": "GET",
      "status_code": 404,
      "error": "Expected 200, got 404"
    }
  ]
}
```

---

## 🛠️ Personalización

### Agregar Nuevos Tests

En `test_suite_completa.py`, añadir a la función `define_test_endpoints()`:

```python
# Nuevo test
EndpointTest(
    method="GET",
    endpoint="/mi-nuevo-endpoint",
    description="Descripción del endpoint",
    requires_auth=True,
    requires_admin=False,
    expected_status=200,
    category="MiCategoria"
)
```

### Cambiar Credenciales

```python
TEST_CREDENTIALS = {
    "superadmin": {
        "email": "tu-admin@email.com",
        "password": "tu-password"
    }
}
```

### Configurar Ambiente

```python
# Para desarrollo local
USE_PRODUCTION = False
DEV_URL = "http://localhost:8000"

# Para producción
USE_PRODUCTION = True
PROD_URL = "https://tu-api.com"
```

---

## 🚨 Troubleshooting

### Problemas Comunes

#### ❌ Error de Autenticación

```
❌ Error crítico: No se pudo configurar autenticación
```

**Solución:**

1. Verificar credenciales en el script
2. Confirmar que el usuario existe en la BD
3. Verificar que la API esté accesible

#### ❌ Connection Error

```
503 Connection error
```

**Solución:**

1. Verificar que la API esté corriendo
2. Confirmar la URL base
3. Revisar firewall/proxy

#### ❌ Timeout

```
408 Request timeout
```

**Solución:**

1. Aumentar timeout en scripts
2. Revisar carga del servidor
3. Optimizar queries lentas

### Logs Detallados

Para debugging, activar logs verbosos:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📞 Soporte

Si tienes problemas con los scripts:

1. **Revisar logs** en consola
2. **Verificar configuración** de URLs y credenciales
3. **Comprobar conectividad** con `curl`
4. **Revisar archivos JSON** de resultados para detalles

---

## 🎯 Roadmap Futuro

- [ ] 🔍 Tests de seguridad automatizados
- [ ] 📱 Tests de endpoints móviles
- [ ] 🤖 Integración con Slack/Teams para alertas
- [ ] 📊 Dashboard web para visualizar resultados
- [ ] 🔄 Tests de regresión automática
- [ ] 📧 Reportes por email programados

---

**Documentación actualizada:** 22 de Julio 2025  
**Versión:** 2.0.0  
**Autor:** API VOLTIO Team
