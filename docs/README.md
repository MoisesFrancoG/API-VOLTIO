# 📚 Documentación API VOLTIO

Esta carpeta contiene toda la documentación completa de la API VOLTIO para desarrolladores frontend.

## 📁 Estructura de Documentación

### 🚀 [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

**📖 Documentación Principal y Guía de Usuario**

- Información general de la API
- Todos los endpoints organizados por módulos
- Ejemplos de requests y responses
- Sistema de autenticación y permisos
- Manejo de errores y códigos de respuesta
- Flujo típico de uso de la aplicación

**👥 Audiencia:** Desarrolladores que necesitan una guía completa para entender e implementar la API

---

### 🔧 [API_TECHNICAL_SCHEMAS.md](./API_TECHNICAL_SCHEMAS.md)

**⚙️ Especificaciones Técnicas y Esquemas de Datos**

- Esquemas detallados de request/response para cada endpoint
- Validaciones de campos específicas
- Relaciones entre entidades de datos
- Restricciones de integridad
- Códigos de respuesta HTTP específicos por endpoint

**👥 Audiencia:** Desarrolladores que necesitan detalles técnicos precisos para la implementación

---

### 💻 [API_FRONTEND_EXAMPLES.md](./API_FRONTEND_EXAMPLES.md)

**🛠️ Ejemplos de Código y Implementación**

- Código JavaScript Vanilla listo para usar
- React Hooks personalizados
- Configuración de Axios con interceptores
- Servicios de autenticación, dispositivos y notificaciones
- Manejo avanzado de errores
- Estilos CSS de ejemplo

**👥 Audiencia:** Desarrolladores que quieren código listo para copiar y adaptar

---

### 📋 [API_QUICK_REFERENCE.md](./API_QUICK_REFERENCE.md)

**⚡ Referencia Rápida y Cheat Sheet**

- Tabla resumen de todos los endpoints
- Códigos de respuesta más comunes
- Ejemplos de cURL listos para usar
- Tips y mejores prácticas
- Referencias de tipos de datos y roles

**👥 Audiencia:** Desarrolladores experimentados que necesitan consultas rápidas durante el desarrollo

---

## 🎯 Cómo Usar Esta Documentación

### 🆕 **Para Desarrolladores Nuevos:**

1. Comenzar con **API_DOCUMENTATION.md** para entender la API
2. Revisar **API_TECHNICAL_SCHEMAS.md** para detalles técnicos
3. Usar **API_FRONTEND_EXAMPLES.md** para implementar
4. Consultar **API_QUICK_REFERENCE.md** para referencias rápidas

### 🚀 **Para Implementación Rápida:**

1. **API_QUICK_REFERENCE.md** → Ver endpoints disponibles
2. **API_FRONTEND_EXAMPLES.md** → Copiar código de servicios
3. **API_TECHNICAL_SCHEMAS.md** → Verificar esquemas específicos

### 🐛 **Para Debugging:**

1. **API_QUICK_REFERENCE.md** → Verificar códigos de error
2. **API_TECHNICAL_SCHEMAS.md** → Validar formato de datos
3. **API_FRONTEND_EXAMPLES.md** → Ver manejo de errores

---

## 🚀 Funcionalidades Principales de la API

### 🔐 **Autenticación y Usuarios**

- Registro y login con JWT
- Gestión de perfiles de usuario
- Sistema de roles (Admin/User)

### 🔌 **Gestión de Dispositivos**

- CRUD completo de dispositivos IoT
- Control de relés ESP32 en tiempo real
- Organización por ubicaciones y tipos

### 📊 **Monitoreo y Lecturas**

- Lecturas de sensores PZEM en tiempo real
- Consultas históricas con filtros
- Datos de consumo eléctrico

### 🔔 **Sistema de Notificaciones**

- Notificaciones personales y de sistema
- Diferentes tipos y prioridades
- Gestión de estado (leído/no leído)

### 🏠 **Configuración del Sistema**

- Gestión de ubicaciones
- Tipos de dispositivos
- Comandos IR personalizados

---

## 🔑 Información de Conexión

**URL Base:** `http://127.0.0.1:8000/api/v1`  
**Documentación Interactiva:** `http://127.0.0.1:8000/docs`  
**Esquema OpenAPI:** `http://127.0.0.1:8000/openapi.json`

---

## 📞 Soporte

Para dudas específicas sobre la implementación:

1. Consultar primero la documentación correspondiente
2. Verificar ejemplos de código en **API_FRONTEND_EXAMPLES.md**
3. Revisar la referencia rápida para casos comunes

---

## 🔄 Actualizaciones

Esta documentación se mantiene actualizada con:

- ✅ Correcciones de seguridad implementadas
- ✅ Sistema de roles clarificado (Admin/User)
- ✅ Endpoints de control de relé ESP32
- ✅ Integración completa con RabbitMQ
- ✅ Validaciones y permisos actualizados

**Fecha de última actualización:** Enero 2025
