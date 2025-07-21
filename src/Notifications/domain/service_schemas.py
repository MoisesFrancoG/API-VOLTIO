"""
Schemas específicos para el servicio de notificaciones automáticas
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class DeviceAlertSchema(BaseModel):
    """Schema para alertas de dispositivos desde RabbitMQ"""
    mac: str = Field(..., description="MAC address del dispositivo")
    error_type: Literal["TIMEOUT", "OFFLINE", "ERROR", "WARNING", "CRITICAL", "MAINTENANCE"] = Field(
        default="TIMEOUT", description="Tipo de error detectado"
    )
    message: str = Field(..., min_length=1, max_length=500,
                         description="Mensaje descriptivo del problema")

    class Config:
        json_schema_extra = {
            "example": {
                "mac": "CC:DB:A7:2F:AE:B0",
                "error_type": "TIMEOUT",
                "message": "El dispositivo 'Luz de la Oficina' ha dejado de reportar datos. Por favor, revisa su conexión y estado físico."
            }
        }


class AlertProcessingResponse(BaseModel):
    """Response del procesamiento de alertas"""
    success: bool
    notification_id: Optional[int] = None
    device_id: Optional[int] = None
    user_id: Optional[int] = None
    email_sent: Optional[bool] = None
    mac: str
    error: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "notification_id": 123,
                "device_id": 45,
                "user_id": 67,
                "email_sent": True,
                "mac": "CC:DB:A7:2F:AE:B0"
            }
        }


class ManualNotificationSchema(BaseModel):
    """Schema para crear notificaciones manuales (uso administrativo)"""
    user_id: int = Field(..., gt=0, description="ID del usuario destinatario")
    message: str = Field(..., min_length=1, max_length=500,
                         description="Mensaje de la notificación")
    device_id: Optional[int] = Field(None, gt=0,
                                     description="ID del dispositivo relacionado (opcional)")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 5,
                "message": "Mantenimiento programado para tu dispositivo mañana a las 10:00 AM",
                "device_id": 12
            }
        }


class BulkReadNotificationsSchema(BaseModel):
    """Schema para marcar múltiples notificaciones como leídas"""
    notification_ids: list[int] = Field(..., min_items=1,
                                        description="Lista de IDs de notificaciones")

    class Config:
        json_schema_extra = {
            "example": {
                "notification_ids": [1, 2, 3, 4, 5]
            }
        }
