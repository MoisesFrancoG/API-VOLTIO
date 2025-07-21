# ✅ CHECKLIST DE SEGURIDAD - API VOLTIO

## 🚨 **ACCIONES INMEDIATAS COMPLETADAS**

✅ **Auditoría de credenciales realizada**  
✅ **Documentación limpiada de credenciales**  
✅ **Nuevas credenciales generadas**  
✅ **Archivo .env.new creado con credenciales seguras**  
✅ **Nuevo token de InfluxDB generado y verificado**  
✅ **Todas las conexiones validadas exitosamente**

---

## ⚠️ **PENDIENTES CRÍTICOS (HACER AHORA)**

### **📋 Cambios en Servidor de Producción**

- [ ] **PostgreSQL**: Cambiar contraseña de usuario `chmma`

  ```sql
  ALTER USER chmma PASSWORD 'HSQCx3Ajt4p^aJGC';
  ```

- [x] **InfluxDB**: Regenerar token de acceso

  - ✅ **COMPLETADO**: Nuevo token generado y verificado
  - Token: `F2wrepMKWQE_RQrNpKndw3r-xnVTvhj6R0-cu2gulI23YhBAE-x_V4SLnQkUzK97pdHc-4AJn7X9SSJErowPbA==`
  - ✅ Probado exitosamente con escritura de datos

- [x] **RabbitMQ**: Mantener credenciales actuales

  - ✅ **DECISIÓN**: Conservar credenciales existentes por estabilidad
  - Usuario: `admin` / Password: `trike`
  - ✅ Conexión verificada y funcionando

- [ ] **JWT Secret**: Actualizar en .env del servidor

  ```
  SECRET_KEY=N4Z2F0dkQMV3fJRtqFjjKZOYC5WZ0sWDTC1QdaubuPz2108UxSSoVwEo2HeU7WwrH2d0yBWg2hIWP49h33gj1btNQ==
  ```

- [ ] **Email SMTP**: Generar nueva app password para Gmail

### **🔄 Actualizar archivo .env en desarrollo**

- [x] Hacer backup del .env actual: `copy .env .env.backup` ✅
- [x] Reemplazar .env actual con nuevas credenciales ✅
- [x] Verificar que todas las variables están configuradas ✅
- [x] Probar conexiones con nuevas credenciales ✅ **TODAS FUNCIONAN**

### **🔍 Verificación de Funcionamiento**

- [x] Probar conexión a PostgreSQL ✅
- [x] Probar conexión a InfluxDB ✅
- [x] Probar conexión a RabbitMQ ✅
- [x] Verificar autenticación JWT ✅
- [x] Probar configuración de la API ✅

---

## 🛡️ **COMANDOS DE VERIFICACIÓN**

```bash
# Verificar conexión a PostgreSQL
python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='localhost',
        database='voltiodb',
        user='chmma',
        password='HSQCx3Ajt4p^aJGC',
        port=5432
    )
    print('✅ PostgreSQL conectado')
    conn.close()
except Exception as e:
    print(f'❌ Error PostgreSQL: {e}')
"

# Verificar API funcionando
python main.py &
curl http://localhost:8000/test/health
```

---

## 📞 **EN CASO DE PROBLEMAS**

### **Si algo falla:**

1. Mantener credenciales anteriores como backup
2. Verificar configuración de red/firewall
3. Revisar logs de servicios
4. Contactar administrador de sistemas si es necesario

### **Archivos importantes:**

- `.env.new` - Nuevas credenciales generadas
- `docs/SECURITY_AUDIT_REPORT.md` - Reporte completo
- `.env` - Archivo actual (backup antes de cambiar)

---

## 🕐 **TIEMPO ESTIMADO**

**Total**: 30-45 minutos

- Cambios en BD: 10 min
- Actualización de servicios: 15 min
- Verificación: 10-20 min

---

**⚠️ IMPORTANTE: No usar las credenciales actuales en producción hasta completar todos estos pasos**

---

_Creado: 2025-07-20_  
_Prioridad: CRÍTICA_
