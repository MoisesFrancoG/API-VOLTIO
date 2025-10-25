"""
Router interno para el servicio de notificaciones automáticas
Este router maneja las llamadas desde RabbitMQ y servicios internos
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from src.core.db import get_database as get_db
from src.core.auth_middleware import get_current_user
from src.Usuarios.domain.entities import User
from ..application.notification_service_dynamic import NotificationService
from ..domain.service_schemas import (
    DeviceAlertSchema,
    AlertProcessingResponse,
    ManualNotificationSchema,
    BulkReadNotificationsSchema
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/internal/notifications",
                   tags=["Internal Notifications"])


@router.post("/service",
             response_model=AlertProcessingResponse,
             summary="Webhook para procesar alertas desde RabbitMQ",
             description="""
             Endpoint interno para procesar alertas de dispositivos.
             
             Este endpoint es llamado por el Consumer de Notificaciones cuando
             recibe un mensaje de RabbitMQ sobre un dispositivo con problemas.
             
             **No requiere autenticación** ya que es un servicio interno.
             
             El proceso completo:
             1. Busca el dispositivo por MAC address
             2. Encuentra al usuario propietario
             3. Crea la notificación en la base de datos
             4. Envía email al usuario
             """)
async def process_device_alert(
    alert_data: DeviceAlertSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Procesa una alerta de dispositivo desde RabbitMQ

    Este endpoint actúa como webhook interno para el Consumer de Notificaciones.
    """
    try:
        notification_service = NotificationService(db)

        # Procesar la alerta en background para no bloquear la respuesta
        def process_alert():
            try:
                return notification_service.process_device_alert(alert_data.dict())
            except Exception as e:
                logger.error(f"Background task error: {str(e)}")
                return {"success": False, "error": str(e), "mac": alert_data.mac}

        background_tasks.add_task(process_alert)

        # Respuesta inmediata para el consumer
        return AlertProcessingResponse(
            success=True,
            mac=alert_data.mac
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing alert: {str(e)}"
        )


@router.post("/service/sync",
             response_model=AlertProcessingResponse,
             summary="Procesar alerta de forma síncrona",
             description="Versión síncrona del procesamiento de alertas para debugging")
async def process_device_alert_sync(
    alert_data: DeviceAlertSchema,
    db: Session = Depends(get_db)
):
    """
    Procesa una alerta de dispositivo de forma síncrona (para debugging)
    """
    try:
        notification_service = NotificationService(db)
        result = notification_service.process_device_alert(alert_data.dict())

        return AlertProcessingResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing alert: {str(e)}"
        )


# Endpoints administrativos (requieren autenticación)
@router.post("/manual",
             summary="Crear notificación manual",
             description="Crear una notificación manual para cualquier usuario (uso administrativo)")
async def create_manual_notification(
    notification_data: ManualNotificationSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crea una notificación manual (solo para administradores)
    """
    # Verificar que el usuario actual es admin (role_id = 1)
    if current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create manual notifications"
        )

    try:
        notification_service = NotificationService(db)
        notification = notification_service.create_manual_notification(
            user_id=notification_data.user_id,
            message=notification_data.message,
            device_id=notification_data.device_id
        )

        if notification:
            return {"success": True, "notification_id": notification.id}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create notification"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating manual notification: {str(e)}"
        )


@router.put("/bulk-read",
            summary="Marcar múltiples notificaciones como leídas",
            description="Marca múltiples notificaciones del usuario actual como leídas")
async def mark_notifications_as_read(
    request_data: BulkReadNotificationsSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Marca múltiples notificaciones como leídas para el usuario actual
    """
    try:
        notification_service = NotificationService(db)
        updated_count = notification_service.mark_notifications_as_read(
            user_id=current_user.id,
            notification_ids=request_data.notification_ids
        )

        return {
            "success": True,
            "updated_count": updated_count,
            "total_requested": len(request_data.notification_ids)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error marking notifications as read: {str(e)}"
        )


@router.get("/health",
            summary="Health check del servicio",
            description="Verifica que el servicio de notificaciones esté funcionando")
async def health_check():
    """
    Health check para verificar que el servicio esté funcionando
    """
    return {
        "status": "healthy",
        "service": "notification-service",
        "version": "1.0.0"
    }
