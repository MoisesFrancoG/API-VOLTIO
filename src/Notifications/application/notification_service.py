"""
Servicio de Notificaciones por Email
Maneja la lógica de negocio para             # Paso 3: Crear la notificación en la base de datos
            notification_data = NotificationCreateInternal(
                user_id=user.id,
                device_id=device.id,
                message=f"[{error_type}] {message}",
                is_read=False
            )
            
            created_notification = self.notification_repo.create(notification_data)        created_notification = self.notification_repo.create(notification_data)
            
            # Paso 4: Enviar email al usuario
            email_sent = self._send_alert_email(automáticas de dispositivos
"""

import smtplib
import logging
from typing import Optional, Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session

from src.Notifications.infrastructure.repositories import NotificationRepository
from src.Sensores.infrastructure.repositories import SQLAlchemyDeviceRepository as DeviceRepository
from src.Usuarios.infrastructure.repositories import SqlAlchemyUserRepository as UserRepository
from src.Notifications.domain.entities import Notification
from src.Notifications.domain.schemas import NotificationCreate, NotificationCreateInternal
from src.core.config import settings


logger = logging.getLogger(__name__)


class NotificationService:
    """Servicio para manejo de notificaciones automáticas y emails"""

    def __init__(self, db: Session):
        self.db = db
        self.notification_repo = NotificationRepository(db)
        self.device_repo = DeviceRepository(db)
        self.user_repo = UserRepository(db)

    def process_device_alert(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una alerta de dispositivo desde RabbitMQ

        Args:
            alert_data: {
                "mac": "CC:DB:A7:2F:AE:B0",
                "error_type": "TIMEOUT", 
                "message": "El dispositivo ha dejado de reportar datos..."
            }

        Returns:
            Dict con resultado del procesamiento
        """
        try:
            mac_address = alert_data.get("mac")
            error_type = alert_data.get("error_type", "UNKNOWN")
            message = alert_data.get("message", "Alerta de dispositivo")

            if not mac_address:
                raise ValueError("MAC address es requerido")

            # Paso 1: Buscar el dispositivo
            device = self.device_repo.get_by_mac_address(mac_address)
            if not device:
                logger.warning(
                    f"Dispositivo con MAC {mac_address} no encontrado")
                return {
                    "success": False,
                    "error": f"Dispositivo con MAC {mac_address} no encontrado",
                    "mac": mac_address
                }

            # Paso 2: Obtener el propietario del dispositivo
            user = self.user_repo.get_by_id(device.user_id)
            if not user:
                logger.warning(
                    f"Usuario {device.user_id} no encontrado para dispositivo {device.id}")
                return {
                    "success": False,
                    "error": f"Usuario propietario no encontrado",
                    "device_id": device.id,
                    "mac": mac_address
                }

            # Paso 3: Crear la notificación en la base de datos
            notification_data = NotificationCreateInternal(
                user_id=user.id,
                device_id=device.id,
                message=f"[{error_type}] {message}",
                is_read=False
            )

            created_notification = self.notification_repo.create(
                notification_data)

            # Paso 4: Enviar email al usuario
            email_sent = self._send_alert_email(
                user_email=user.email,
                user_name=user.username,
                device_name=device.name or f"Dispositivo {mac_address}",
                mac_address=mac_address,
                error_type=error_type,
                message=message
            )

            logger.info(
                f"Alerta procesada - Device: {device.id}, User: {user.id}, Email: {email_sent}")

            return {
                "success": True,
                "notification_id": created_notification.id,
                "device_id": device.id,
                "user_id": user.id,
                "email_sent": email_sent,
                "mac": mac_address
            }

        except Exception as e:
            logger.error(f"Error procesando alerta: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "mac": alert_data.get("mac", "unknown")
            }

    def _send_alert_email(
        self,
        user_email: str,
        user_name: str,
        device_name: str,
        mac_address: str,
        error_type: str,
        message: str
    ) -> bool:
        """
        Envía email de alerta al usuario

        Returns:
            bool: True si el email se envió correctamente
        """
        try:
            # Configuración del servidor SMTP desde settings
            if not settings.notification_email_enabled:
                logger.warning(
                    "Configuración SMTP incompleta, email no enviado")
                return False

            # Crear el mensaje
            msg = MIMEMultipart()
            msg['From'] = settings.from_email
            msg['To'] = user_email
            msg['Subject'] = f"🚨 Alerta VOLTIO - Problema con {device_name}"

            # Cuerpo del email en HTML
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #dc3545; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f8f9fa; }}
                    .device-info {{ background-color: white; padding: 15px; border-left: 4px solid #dc3545; margin: 15px 0; }}
                    .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                    .alert-type {{ color: #dc3545; font-weight: bold; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>⚠️ ALERTA VOLTIO</h1>
                        <p>Sistema de Monitoreo de Dispositivos</p>
                    </div>
                    
                    <div class="content">
                        <h2>Hola {user_name},</h2>
                        
                        <p>Hemos detectado un problema con uno de tus dispositivos:</p>
                        
                        <div class="device-info">
                            <h3>📱 Información del Dispositivo</h3>
                            <p><strong>Nombre:</strong> {device_name}</p>
                            <p><strong>MAC Address:</strong> {mac_address}</p>
                            <p><strong>Tipo de Alerta:</strong> <span class="alert-type">{error_type}</span></p>
                        </div>
                        
                        <div class="device-info">
                            <h3>📋 Descripción del Problema</h3>
                            <p>{message}</p>
                        </div>
                        
                        <h3>🔧 Acciones Recomendadas</h3>
                        <ul>
                            <li>Verifica que el dispositivo esté encendido y conectado</li>
                            <li>Revisa la conexión Wi-Fi del dispositivo</li>
                            <li>Asegúrate de que no haya interferencias en la red</li>
                            <li>Si el problema persiste, contacta al soporte técnico</li>
                        </ul>
                        
                        <p><strong>Nota:</strong> Esta notificación también está disponible en tu panel de control de VOLTIO.</p>
                    </div>
                    
                    <div class="footer">
                        <p>Este es un email automático del Sistema VOLTIO</p>
                        <p>No respondas a este correo</p>
                    </div>
                </div>
            </body>
            </html>
            """

            msg.attach(MIMEText(html_body, 'html'))

            # Enviar el email
            with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(msg)

            logger.info(f"Email enviado exitosamente a {user_email}")
            return True

        except Exception as e:
            logger.error(f"Error enviando email a {user_email}: {str(e)}")
            return False

    def create_manual_notification(
        self,
        user_id: int,
        message: str,
        device_id: Optional[int] = None
    ) -> Optional[Notification]:
        """
        Crea una notificación manual (para uso administrativo)
        """
        try:
            notification_data = NotificationCreateInternal(
                user_id=user_id,
                device_id=device_id,
                message=message
            )

            return self.notification_repo.create(notification_data)

        except Exception as e:
            logger.error(f"Error creando notificación manual: {str(e)}")
            return None

    def mark_notifications_as_read(self, user_id: int, notification_ids: list[int]) -> int:
        """
        Marca múltiples notificaciones como leídas

        Returns:
            int: Número de notificaciones actualizadas
        """
        try:
            updated_count = 0
            for notification_id in notification_ids:
                notification = self.notification_repo.get_by_id(
                    notification_id, user_id)
                if notification and notification.user_id == user_id:
                    notification.is_read = True
                    self.notification_repo.update(
                        notification_id, notification)
                    updated_count += 1

            return updated_count

        except Exception as e:
            logger.error(
                f"Error marcando notificaciones como leídas: {str(e)}")
            return 0
