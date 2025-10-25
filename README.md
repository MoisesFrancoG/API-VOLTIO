# API VOLTIO v1.2.0

API FastAPI para gestión de sensores IoT con conectividad a PostgreSQL e InfluxDB.

## 📚 Documentación Completa para Frontend

**🎯 Nueva documentación completa disponible en:**

### **📁 [/docs](./docs/)**

- **📖 [Documentación Principal](./docs/API_DOCUMENTATION.md)** - Guía completa de la API
- **🔧 [Esquemas Técnicos](./docs/API_TECHNICAL_SCHEMAS.md)** - Especificaciones detalladas
- **💻 [Ejemplos de Código](./docs/API_FRONTEND_EXAMPLES.md)** - Código listo para usar
- **📋 [Referencia Rápida](./docs/API_QUICK_REFERENCE.md)** - Cheat sheet de endpoints

**✨ Incluye:**

- ✅ **50+ endpoints** documentados con ejemplos
- ✅ **Código JavaScript/React** listo para copiar
- ✅ **Sistema de autenticación** JWT completo
- ✅ **Control de relés ESP32** via RabbitMQ
- ✅ **Esquemas de validación** detallados
- ✅ **Sistema de permisos** y roles clarificado

---

## Estructura del Proyecto

```
API-VOLTIO/
├── src/                     # Código fuente principal
│   ├── Alertas/            # Módulo de alertas
│   ├── ComandosIR/         # Comandos infrarrojos
│   ├── Lecturas/           # Lecturas de sensores (PostgreSQL)
│   ├── Lecturas_influx_pzem/ # Lecturas PZEM (InfluxDB)
│   ├── Sensores/           # Gestión de sensores
│   ├── TipoSensores/       # Tipos de sensores
│   ├── Ubicaciones/        # Ubicaciones
│   ├── Usuarios/           # Gestión de usuarios
│   ├── Roles/              # Sistema de roles
│   └── core/               # Configuración central
├── tests/                  # Tests organizados por categoría
│   ├── unit/               # Tests unitarios por módulo
│   ├── integration/        # Tests de integración
│   ├── deployment/         # Tests de validación de despliegue
│   ├── test_*.py           # Tests específicos del proyecto
├── docs/                   # Documentación completa
│   ├── api/                # Documentación de API
│   ├── deployment/         # Guías de despliegue
│   ├── guides/             # Guías de uso
│   ├── *.md                # Documentación principal de API
│   └── demo_*.py           # Archivos de demostración
├── scripts/                # Scripts utilitarios
│   ├── deployment/         # Scripts de despliegue
│   ├── database/           # Scripts de BD
│   └── development/        # Scripts de desarrollo
├── configs/                # Configuraciones
│   ├── nginx/              # Configuración Nginx
│   ├── supervisor/         # Configuración Supervisor
│   └── ssh/                # Claves SSH
├── venv/                   # Entorno virtual Python
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias Python
├── run_all_tests.py        # Ejecutor de tests
├── .github/                # GitHub Actions CI/CD
└── README.md               # Este archivo
```

## Inicio Rápido

1. **Instalación**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configuración**:

   - Copiar `.env.example` a `.env`
   - Configurar variables de entorno

3. **Ejecutar**:

   ```bash
   python main.py
   ```

4. **Documentación API**: `http://localhost:8000/docs`

## Endpoints de Prueba

La API incluye 9 endpoints de validación para verificar el estado del sistema:

- `/test/health` - Estado básico de la API
- `/test/deployment-v2` - Validación completa de despliegue
- `/test/system-info` - Información del sistema
- `/test/database-check` - Estado de las bases de datos
- `/test/environment-vars` - Variables de entorno
- `/test/api-performance` - Rendimiento de la API
- `/test/all-endpoints` - Resumen de todos los endpoints

## Despliegue

- **Desarrollo**: Ver `scripts/development/`
- **Producción**: Ver `docs/deployment/`
- **CI/CD**: GitHub Actions configurado

## Versión

**v1.2.0** - Incluye endpoints de validación completos y estructura organizada

---

Para más información, consultar la documentación en `docs/`
