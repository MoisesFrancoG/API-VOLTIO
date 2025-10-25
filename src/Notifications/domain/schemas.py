"""
Validation and data transfer schemas for Notification (Pydantic)
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class NotificationBase(BaseModel):
    user_id: int = Field(..., gt=0,
                         description="ID del usuario que recibe la notificación")
    device_id: Optional[int] = Field(
        None, gt=0, description="ID del dispositivo relacionado (opcional)")
    message: str = Field(..., min_length=1, max_length=500,
                         description="Mensaje de la notificación")
    is_read: bool = Field(
        default=False, description="Estado de lectura de la notificación")

    class Config:
        from_attributes = True  # Allows working with ORM objects like SQLAlchemy


class NotificationCreate(BaseModel):
    """Schema for creating a new notification - user_id taken from auth"""
    device_id: Optional[int] = Field(
        None, gt=0, description="ID del dispositivo relacionado (opcional)")
    message: str = Field(..., min_length=1, max_length=500,
                         description="Mensaje de la notificación")
    is_read: bool = Field(
        default=False, description="Estado de lectura de la notificación")

    class Config:
        from_attributes = True


class NotificationCreateInternal(BaseModel):
    """Schema for creating notifications internally (with user_id)"""
    user_id: int = Field(..., gt=0, description="ID del usuario destinatario")
    device_id: Optional[int] = Field(
        None, gt=0, description="ID del dispositivo relacionado (opcional)")
    message: str = Field(..., min_length=1, max_length=500,
                         description="Mensaje de la notificación")
    is_read: bool = Field(
        default=False, description="Estado de lectura de la notificación")

    class Config:
        from_attributes = True


class NotificationUpdate(BaseModel):
    """Schema for updating a notification"""
    message: Optional[str] = Field(None, min_length=1, max_length=500)
    is_read: Optional[bool] = None

    class Config:
        from_attributes = True


class NotificationResponse(NotificationBase):
    """Response schema for displaying a notification"""
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NotificationMarkAsRead(BaseModel):
    """Schema for marking notification as read"""
    is_read: bool = Field(
        default=True, description="Marcar como leída o no leída")


class NotificationFilters(BaseModel):
    """Schema for filtering notifications"""
    is_read: Optional[bool] = Field(
        None, description="Filtrar por estado de lectura")
    device_id: Optional[int] = Field(
        None, gt=0, description="Filtrar por dispositivo")
    limit: int = Field(default=50, ge=1, le=100,
                       description="Límite de resultados")
    offset: int = Field(
        default=0, ge=0, description="Desplazamiento para paginación")
