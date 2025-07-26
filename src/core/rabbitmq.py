"""
Configuración y cliente de RabbitMQ para envío de comandos a dispositivos
"""
import os
import json
import logging
from typing import Optional
import pika
from pika.exceptions import AMQPConnectionError, AMQPChannelError

logger = logging.getLogger(__name__)


class RabbitMQClient:
    """Cliente para conectar y publicar mensajes en RabbitMQ"""

    def __init__(self):
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[pika.channel.Channel] = None
        self._setup_connection()

    def _setup_connection(self):
        """Configurar conexión a RabbitMQ"""
        try:
            # Configuración desde variables de entorno
            host = os.getenv('RABBITMQ_HOST', 'localhost')
            port = int(os.getenv('RABBITMQ_PORT', '5672'))
            username = os.getenv('RABBITMQ_USERNAME', 'guest')
            password = os.getenv('RABBITMQ_PASSWORD', 'guest')
            vhost = os.getenv('RABBITMQ_VHOST', '/')

            # Crear credenciales
            credentials = pika.PlainCredentials(username, password)

            # Parámetros de conexión
            parameters = pika.ConnectionParameters(
                host=host,
                port=port,
                virtual_host=vhost,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )

            # Establecer conexión
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

            logger.info(f"✅ Conectado a RabbitMQ en {host}:{port}")

        except AMQPConnectionError as e:
            logger.error(f"❌ Error de conexión a RabbitMQ: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado al conectar a RabbitMQ: {e}")
            raise

    def publish_device_command(
        self,
        mac_address: str,
        command: str,
        exchange: str = "amq.topic",
        command_type: str = "relay"  # "relay" o "ir"
    ) -> bool:
        """
        Publica un comando a un dispositivo específico

        Args:
            mac_address: Dirección MAC del dispositivo
            command: Comando a enviar ("ON" o "OFF")
            exchange: Exchange de RabbitMQ (por defecto "amq.topic")
            command_type: "relay" para relé, "ir" para IR

        Returns:
            bool: True si se publicó exitosamente, False en caso contrario
        """
        try:
            if not self.channel:
                self._setup_connection()

            # Construir routing key según tipo de comando
            if command_type == "relay":
                routing_key = f"pzem.command.{mac_address}"
            elif command_type == "ir":
                routing_key = f"ir.command.{mac_address}"
            else:
                logger.error(f"❌ Tipo de comando desconocido: {command_type}")
                return False

            # Publicar mensaje
            # Invertir el comando para relay, para IR se envía tal cual
            if command_type == "relay":
                inverted_command = "OFF" if command == "ON" else "ON" if command == "OFF" else command
            else:
                inverted_command = command

            self.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=inverted_command,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Hacer el mensaje persistente
                    content_type='text/plain',
                    timestamp=int(os.urandom(4).hex(), 16)  # Timestamp único
                )
            )

            logger.info(
                f"📤 Comando '{command}' enviado a dispositivo {mac_address} en {routing_key} con exchange {exchange}")
            return True

        except AMQPChannelError as e:
            logger.error(f"❌ Error de canal RabbitMQ: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error al publicar comando: {e}")
            return False

    def close(self):
        """Cerrar conexión a RabbitMQ"""
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                logger.info("🔌 Conexión a RabbitMQ cerrada")
        except Exception as e:
            logger.warning(f"⚠️ Error al cerrar conexión RabbitMQ: {e}")


# Instancia global del cliente
_rabbitmq_client: Optional[RabbitMQClient] = None


def get_rabbitmq_client() -> RabbitMQClient:
    """
    Obtener instancia singleton del cliente RabbitMQ

    Returns:
        RabbitMQClient: Instancia del cliente
    """
    global _rabbitmq_client

    if _rabbitmq_client is None:
        _rabbitmq_client = RabbitMQClient()

    return _rabbitmq_client


def publish_relay_command(mac_address: str, action: str) -> bool:
    """
    Función helper para publicar comandos de relé

    Args:
        mac_address: Dirección MAC del dispositivo
        action: Acción a realizar ("ON" o "OFF")

    Returns:
        bool: True si se envió exitosamente
    """
    try:
        client = get_rabbitmq_client()
        return client.publish_device_command(mac_address, action, command_type="relay")
    except Exception as e:
        logger.error(f"❌ Error al enviar comando de relé: {e}")
        return False


def publish_ir_command(mac_address: str, action: str) -> bool:
    """
    Función helper para publicar comandos IR

    Args:
        mac_address: Dirección MAC del dispositivo
        action: Acción a realizar ("ON" o "OFF")

    Returns:
        bool: True si se envió exitosamente
    """
    try:
        client = get_rabbitmq_client()
        return client.publish_device_command(mac_address, action, command_type="ir")
    except Exception as e:
        logger.error(f"❌ Error al enviar comando IR: {e}")
        return False
