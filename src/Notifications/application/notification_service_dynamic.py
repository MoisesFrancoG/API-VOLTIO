"""
Servicio de Notificaciones por Email con Templates Dinámicos
Maneja la lógica de negocio para notificaciones automáticas de dispositivos
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
from src.Notifications.infrastructure.email_templates import EmailTemplateService
from src.core.config import settings

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Servicio para procesar alertas de dispositivos y enviar notificaciones por email
    """

    def __init__(self, db: Session):
        self.db = db
        self.notification_repo = NotificationRepository(db)
        self.device_repo = DeviceRepository(db)
        self.user_repo = UserRepository(db)
        self.email_template_service = EmailTemplateService()

    def process_device_alert(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una alerta de dispositivo y envía notificación por email

        Args:
            alert_data: Diccionario con 'mac', 'error_type', 'message'

        Returns:
            Dict con el resultado del procesamiento
        """
        try:
            mac = alert_data.get('mac')
            error_type = alert_data.get('error_type', 'ERROR')
            message = alert_data.get(
                'message', 'Problema detectado en el dispositivo')

            logger.info(
                f"Procesando alerta para MAC: {mac}, Tipo: {error_type}")

            # Paso 1: Buscar el dispositivo por MAC
            device = self.device_repo.get_by_mac_address(mac)
            if not device:
                logger.warning(f"Dispositivo no encontrado para MAC: {mac}")
                return {
                    "success": False,
                    "error": f"Device not found for MAC: {mac}",
                    "mac": mac
                }

            # Paso 2: Obtener el usuario propietario del dispositivo
            user = self.user_repo.get_by_id(device.user_id)
            if not user:
                logger.warning(
                    f"Usuario no encontrado para device ID: {device.id}")
                return {
                    "success": False,
                    "error": f"User not found for device ID: {device.id}",
                    "mac": mac,
                    "device_id": device.id
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

            # Paso 4: Enviar email al usuario con template dinámico
            email_sent = self._send_dynamic_alert_email(
                user_email=user.email,
                user_name=user.username,  # Cambiado de user.name a user.username
                device_name=device.name,
                mac_address=mac,
                error_type=error_type,
                message=message
            )

            logger.info(
                f"Alerta procesada exitosamente - Notification ID: {created_notification.id}")

            return {
                "success": True,
                "notification_id": created_notification.id,
                "device_id": device.id,
                "user_id": user.id,
                "email_sent": email_sent,
                "mac": mac
            }

        except Exception as e:
            logger.error(f"Error procesando alerta: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "mac": alert_data.get('mac', 'unknown')
            }

    def _send_dynamic_alert_email(
        self,
        user_email: str,
        user_name: str,
        device_name: str,
        mac_address: str,
        error_type: str,
        message: str
    ) -> bool:
        """
        Envía un email con template HTML dinámico según el tipo de alerta
        """
        try:
            # Crear el mensaje de email
            msg = MIMEMultipart('alternative')

            # Obtener configuración específica del tipo de alerta
            alert_config = self.email_template_service.get_alert_config(
                error_type)

            msg['Subject'] = f"{alert_config['emoji']} {alert_config['title']} - {device_name}"
            msg['From'] = settings.from_email
            msg['To'] = user_email

            # Generar HTML dinámico
            html_body = self.email_template_service.generate_dynamic_html(
                user_name=user_name,
                device_name=device_name,
                mac_address=mac_address,
                error_type=error_type,
                message=message
            )

            msg.attach(MIMEText(html_body, 'html'))

            # Enviar el email
            with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(msg)

            logger.info(
                f"Email dinámico enviado exitosamente a {user_email} - Tipo: {error_type}")
            return True

        except Exception as e:
            logger.error(
                f"Error enviando email dinámico a {user_email}: {str(e)}")
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

    def mark_notifications_as_read(
        self,
        user_id: int,
        notification_ids: list
    ) -> int:
        """
        Marca múltiples notificaciones como leídas
        """
        try:
            updated_count = 0
            for notification_id in notification_ids:
                notification = self.notification_repo.get_by_id_and_user(
                    notification_id, user_id
                )
                if notification and not notification.is_read:
                    notification.is_read = True
                    self.notification_repo.update(notification)
                    updated_count += 1

            self.db.commit()
            return updated_count

        except Exception as e:
            logger.error(
                f"Error marcando notificaciones como leídas: {str(e)}")
            self.db.rollback()
            return 0

    def send_test_email(
        self,
        user_email: str,
        error_type: str = "TIMEOUT"
    ) -> bool:
        """
        Envía un email de prueba con el template dinámico
        """
        return self._send_dynamic_alert_email(
            user_email=user_email,
            user_name="Usuario de Prueba",
            device_name="Dispositivo de Prueba",
            mac_address="AA:BB:CC:DD:EE:FF",
            error_type=error_type,
            message=f"Este es un email de prueba para el tipo de alerta: {error_type}"
        )
