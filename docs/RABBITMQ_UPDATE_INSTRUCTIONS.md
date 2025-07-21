# 🚨 INSTRUCCIONES PARA ACTUALIZAR RABBITMQ

## 📋 **PROBLEMA DETECTADO**

❌ **RabbitMQ rechaza la nueva contraseña generada**  
La contraseña `GWQ32vbwGexPPJb2wNGFD` no está configurada en el servidor.

---

## 🔧 **SOLUCIÓN: Actualizar contraseña en servidor RabbitMQ**

### **Opción A: Cambiar contraseña existente**

```bash
# Conectar al servidor RabbitMQ (52.73.74.139)
ssh -i "ruta_a_tu_clave.pem" ubuntu@52.73.74.139

# Cambiar contraseña del usuario admin
sudo rabbitmqctl change_password admin GWQ32vbwGexPPJb2wNGFD

# Verificar usuarios
sudo rabbitmqctl list_users
```

### **Opción B: Mantener contraseña actual (TEMPORAL)**

Si no puedes acceder al servidor RabbitMQ ahora mismo, puedes mantener la contraseña actual temporalmente:

**Actualizar `.env.new` con credenciales actuales:**

```bash
RABBITMQ_PASSWORD=trike
```

---

## 🎯 **DECISIÓN TOMADA**

✅ **MANTENER CREDENCIALES ACTUALES DE RABBITMQ**

**Razones:**

- Estabilidad del sistema en producción
- Evitar interrupciones del servicio
- Las credenciales actuales no están comprometidas públicamente

**Configuración final:**

```bash
RABBITMQ_USERNAME=admin
RABBITMQ_PASSWORD=trike
```

---

## 📝 **COMANDOS DE VERIFICACIÓN**

```bash
# Probar conexión manual a RabbitMQ
python -c "
import pika
try:
    credentials = pika.PlainCredentials('admin', 'CONTRASEÑA_ACTUAL')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='52.73.74.139',
            port=5672,
            credentials=credentials
        )
    )
    print('✅ RabbitMQ conectado')
    connection.close()
except Exception as e:
    print(f'❌ Error: {e}')
"
```

---

**⏰ Estado**: Pendiente de actualización en servidor
**🔑 Nueva contraseña**: `GWQ32vbwGexPPJb2wNGFD`
