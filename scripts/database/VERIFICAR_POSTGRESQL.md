# Configurar API sin Túnel SSH y Reiniciar

## 1. Conectar al servidor
```bash
ssh -i voltioBD.pem ubuntu@voltioapi.acstree.xyz
```

## 2. Acceder al usuario deploy
```bash
sudo su - deploy
cd /home/deploy/API-VOLTIO
```

## 2.1. Configurar conexión directa a PostgreSQL (SIN túnel SSH)
```bash
# Editar el archivo .env
nano .env

# Cambiar estas configuraciones:
# SSH_TUNNEL_ENABLED=false
# DB_HOST=13.222.89.227
# DB_PORT=5432
# DB_USER=chmma
# DB_PASSWORD=HSQCx3Ajt4p^aJGC
# DB_NAME=voltiodb
```

## 2.2. Archivo .env completo para conexión directa
```bash
cat > .env << 'EOF'
# Database Configuration - Conexión Directa
SSH_TUNNEL_ENABLED=false
DB_HOST=13.222.89.227
DB_PORT=5432
DB_USER=chmma
DB_PASSWORD=HSQCx3Ajt4p^aJGC
DB_NAME=voltiodb

# InfluxDB Configuration
INFLUXDB_URL=http://52.201.107.193:8086
INFLUXDB_TOKEN=tu_token_aqui
INFLUXDB_ORG=voltio
INFLUXDB_BUCKET=sensor_data

# RabbitMQ Configuration
RABBITMQ_HOST=52.73.74.139
RABBITMQ_PORT=5672
RABBITMQ_USER=admin
RABBITMQ_PASSWORD=trike

# API Configuration
SECRET_KEY=tu_secret_key_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF
```

## 3. Verificar conectividad a PostgreSQL
```bash
# Probar conexión directa desde el servidor
telnet 13.222.89.227 5432

# O usar nc (netcat)
nc -zv 13.222.89.227 5432

# Verificar que PostgreSQL acepta conexiones remotas
psql -h 13.222.89.227 -p 5432 -U chmma -d voltiodb
```

## 4. Reiniciar el servicio voltio-api
```bash
# Con supervisor (si está configurado)
sudo supervisorctl restart voltio-api

# O con systemctl (si es un servicio systemd)
sudo systemctl restart voltio-api

# O detener y iniciar manualmente
sudo supervisorctl stop voltio-api
sudo supervisorctl start voltio-api
```

## 5. Verificar el estado del servicio
```bash
# Estado del servicio
sudo supervisorctl status voltio-api

# Ver logs en tiempo real
sudo supervisorctl tail -f voltio-api

# O con systemctl
sudo systemctl status voltio-api
sudo journalctl -u voltio-api -f
```

## 6. Verificar que la API responde
```bash
curl -X GET "https://voltioapi.acstree.xyz/docs"
curl -X GET "https://voltioapi.acstree.xyz/health"
```

## Comandos rápidos para cambiar configuración:
```bash
# Comando completo para actualizar .env y reiniciar
ssh -i voltioBD.pem ubuntu@voltioapi.acstree.xyz '
sudo su - deploy -c "
cd /home/deploy/API-VOLTIO
sed -i \"s/SSH_TUNNEL_ENABLED=true/SSH_TUNNEL_ENABLED=false/g\" .env
sed -i \"s/DB_HOST=localhost/DB_HOST=13.222.89.227/g\" .env
sudo supervisorctl restart voltio-api
"'
```

## Troubleshooting PostgreSQL
Si hay problemas de conexión, verificar:

1. **Firewall del servidor PostgreSQL** - Puerto 5432 debe estar abierto
2. **Configuración pg_hba.conf** - Debe permitir conexiones desde la IP del servidor API
3. **postgresql.conf** - `listen_addresses` debe incluir la IP o '*'

```bash
# Verificar si el puerto está abierto desde el servidor API
nmap -p 5432 13.222.89.227

# Test de conectividad básica
ping 13.222.89.227
```
