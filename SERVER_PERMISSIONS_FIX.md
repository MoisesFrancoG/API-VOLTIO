# 🔧 SOLUCIÓN DE PERMISOS - SERVIDOR EC2

## 🚨 **Problema Identificado:**

```bash
-bash: cd: /home/deploy/API-VOLTIO: Permission denied
cat: .env: No such file or directory
```

## 🛠️ **COMANDOS DE REPARACIÓN:**

### 1️⃣ **Verificar Usuario Actual:**

```bash
whoami
id
```

### 2️⃣ **Verificar Estructura de Directorios:**

```bash
# Ver qué hay en /home
ls -la /home/

# Ver permisos del directorio deploy
ls -la /home/ | grep deploy
```

### 3️⃣ **Verificar Directorio API-VOLTIO:**

```bash
# Buscar dónde está realmente el proyecto
find /home -name "API-VOLTIO" -type d 2>/dev/null

# Otra búsqueda
find / -name "API-VOLTIO" -type d 2>/dev/null | head -10
```

### 4️⃣ **Comandos de Reparación de Permisos:**

**Opción A - Si el directorio existe pero sin permisos:**

```bash
# Cambiar propietario (ejecutar como sudo)
sudo chown -R ubuntu:ubuntu /home/deploy/API-VOLTIO

# Cambiar permisos
sudo chmod -R 755 /home/deploy/API-VOLTIO

# Verificar
ls -la /home/deploy/
```

**Opción B - Si el directorio no existe:**

```bash
# Crear directorio con permisos correctos
sudo mkdir -p /home/deploy/API-VOLTIO
sudo chown ubuntu:ubuntu /home/deploy/API-VOLTIO
sudo chmod 755 /home/deploy/API-VOLTIO
```

### 5️⃣ **Verificar Servicios y Procesos:**

```bash
# Ver si la aplicación está corriendo
ps aux | grep python
ps aux | grep voltio

# Ver servicios supervisor
sudo supervisorctl status

# Ver servicios systemd
systemctl --user list-units | grep voltio
sudo systemctl list-units | grep voltio
```

### 6️⃣ **Buscar Archivos de Configuración:**

```bash
# Buscar archivos .env
find /home -name ".env" -type f 2>/dev/null
find /opt -name ".env" -type f 2>/dev/null

# Buscar main.py
find /home -name "main.py" -type f 2>/dev/null
find /opt -name "main.py" -type f 2>/dev/null
```

### 7️⃣ **Verificar Ubicación Real del Proyecto:**

```bash
# Comprobar configuración supervisor
sudo cat /etc/supervisor/conf.d/voltio-api.conf 2>/dev/null

# Comprobar configuración systemd
sudo cat /etc/systemd/system/voltio-api.service 2>/dev/null
```

## 🎯 **SECUENCIA COMPLETA DE COMANDOS:**

**Ejecuta estos comandos uno por uno:**

```bash
# 1. Verificar usuario
echo "Usuario actual: $(whoami)"

# 2. Buscar proyecto
echo "Buscando API-VOLTIO..."
find /home -name "API-VOLTIO" -type d 2>/dev/null

# 3. Ver estructura /home
ls -la /home/

# 4. Verificar permisos deploy
ls -la /home/ | grep deploy

# 5. Intentar crear/reparar directorio
sudo mkdir -p /home/deploy/API-VOLTIO
sudo chown ubuntu:ubuntu /home/deploy/API-VOLTIO
sudo chmod 755 /home/deploy/API-VOLTIO

# 6. Verificar aplicación corriendo
ps aux | grep python | grep -v grep

# 7. Ver configuración supervisor
sudo supervisorctl status

# 8. Buscar archivos del proyecto
find /home -name "main.py" -type f 2>/dev/null
```

## 🔍 **Posibles Ubicaciones del Proyecto:**

- `/home/ubuntu/API-VOLTIO`
- `/home/deploy/API-VOLTIO`
- `/opt/API-VOLTIO`
- `/var/www/API-VOLTIO`
- `/srv/API-VOLTIO`

## 📝 **Siguiente Paso:**

Una vez que encuentres la ubicación correcta del proyecto y repares los permisos, podrás:

1. Acceder al directorio del proyecto
2. Verificar el archivo `.env`
3. Comprobar las credenciales de base de datos
4. Reiniciar los servicios si es necesario

---

**Ejecuta los comandos paso a paso y reporta los resultados para continuar con la reparación.**
