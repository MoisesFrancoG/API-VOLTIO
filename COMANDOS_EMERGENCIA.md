# Comandos de emergencia para EC2

## 🚨 Si el despliegue falla

### 1. Conectar al servidor
```bash
ssh -i "voltioBD.pem" ubuntu@voltio_api.acstree.xyz
```

### 2. Ejecutar script de solución automática
```bash
# Cambiar a usuario deploy
sudo su - deploy

# Ejecutar script de solución
cd API-VOLTIO
wget -O fix-deployment.sh https://raw.githubusercontent.com/MoisesFrancoG/API-VOLTIO/develop/scripts/fix-deployment.sh
chmod +x fix-deployment.sh
./fix-deployment.sh
```

### 3. Solución manual paso a paso

```bash
# Ir al directorio del proyecto
cd /home/deploy/API-VOLTIO

# Guardar cambios locales
git stash

# Actualizar código
git pull origin develop

# Reinstalar dependencias
source venv/bin/activate
pip install -r requirements.txt

# Reiniciar aplicación
sudo supervisorctl restart voltio-api

# Verificar que funciona
curl http://localhost:8000/
```

### 4. Si requirements.txt está corrupto

```bash
# Crear requirements.txt limpio
cat > requirements.txt << 'EOF'
fastapi==0.115.14
uvicorn==0.35.0
pydantic==2.11.7
sqlalchemy==2.0.36
psycopg2-binary==2.9.10
influxdb-client==1.44.0
python-dotenv==1.0.1
passlib[bcrypt]==1.7.4
python-multipart==0.0.17
email-validator==2.2.0
python-jose[cryptography]==3.3.0
bcrypt==4.2.0
pydantic-settings==2.3.4
psutil==6.1.0
EOF

# Reinstalar dependencias
pip install -r requirements.txt
```

### 5. Reset completo (última opción)

```bash
# CUIDADO: Esto elimina todos los cambios locales
cd /home/deploy/API-VOLTIO
git fetch origin
git reset --hard origin/develop
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
sudo supervisorctl restart voltio-api
```

### 6. Verificar logs

```bash
# Ver logs de la aplicación
sudo supervisorctl tail -f voltio-api

# Ver logs de Nginx
sudo tail -f /var/log/nginx/voltio-api.error.log

# Ver estado de servicios
sudo supervisorctl status
sudo systemctl status nginx
```
