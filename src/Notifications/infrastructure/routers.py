"""
Rutas FastAPI para el módulo de Notificaciones
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.core.db import get_database
from src.core.auth_middleware import get_current_user
from src.Usuarios.domain.schemas import UserResponse
from src.Notifications.domain.schemas import (
    NotificationCreate, NotificationUpdate, NotificationResponse,
    NotificationFilters, NotificationMarkAsRead
)
from src.Notifications.application.use_cases import NotificationUseCases
from src.Notifications.infrastructure.database import get_notification_use_cases


router = APIRouter(prefix="/notifications", tags=["Notifications"])


def get_use_cases(db: Session = Depends(get_database)) -> NotificationUseCases:
    """Dependency para obtener los casos de uso de Notification"""
    return get_notification_use_cases(db)


@router.get(
    "/",
    response_model=List[NotificationResponse],
    summary="Listar notificaciones del usuario",
    description="Obtiene las notificaciones del usuario autenticado con filtros opcionales"
)
def list_user_notifications(
    is_read: Optional[bool] = Query(
        None, description="Filtrar por estado de lectura"),
    device_id: Optional[int] = Query(
        None, description="Filtrar por dispositivo"),
    limit: int = Query(50, ge=1, le=100, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Desplazamiento para paginación"),
    current_user: UserResponse = Depends(get_current_user),
    use_cases: NotificationUseCases = Depends(get_use_cases)
):
    filters = NotificationFilters(
        is_read=is_read,
        device_id=device_id,
        limit=limit,
        offset=offset
    )
    return use_cases.get_user_notifications(current_user.id, filters)


@router.get(
    "/unread-count",
    response_model=int,
    summary="Contar notificaciones no leídas",
    description="Obtiene el número de notificaciones no leídas del usuario"
)
def get_unread_count(
    current_user: UserResponse = Depends(get_current_user),
    use_cases: NotificationUseCases = Depends(get_use_cases)
):
    return use_cases.get_unread_count(current_user.id)


@router.post(
    "/",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear notificación",
    description="Crea una nueva notificación para el usuario autenticado"
)
def create_notification(
    notification: NotificationCreate,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: NotificationUseCases = Depends(get_use_cases)
):
    # Crear NotificationCreate completa con user_id del usuario autenticado
    from src.Notifications.domain.schemas import NotificationBase
    notification_with_user = NotificationBase(
        user_id=current_user.id,  # ✅ Tomado automáticamente del token
        device_id=notification.device_id,
        message=notification.message,
        is_read=notification.is_read
    )

    return use_cases.create_notification(notification_with_user)


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
    summary="Obtener notificación específica",
    description="Obtiene una notificación específica del usuario"
)
def get_notification(
    notification_id: int,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: NotificationUseCases = Depends(get_use_cases)
):
    notification = use_cases.get_notification(notification_id, current_user.id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada"
        )
    return notification


@router.put(
    "/{notification_id}",
    response_model=NotificationResponse,
    summary="Actualizar notificación",
    description="Actualiza una notificación del usuario"
)
def update_notification(
    notification_id: int,
    notification_update: NotificationUpdate,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: NotificationUseCases = Depends(get_use_cases)
):
    updated_notification = use_cases.update_notification(
        notification_id, current_user.id, notification_update
    )
    if not updated_notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada"
        )
    return updated_notification


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
    summary="Marcar notificación como leída",
    description="Marca una notificación específica como leída"
)
def mark_notification_as_read(
    notification_id: int,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: NotificationUseCases = Depends(get_use_cases)
):
    updated_notification = use_cases.mark_as_read(
        notification_id, current_user.id)
    if not updated_notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada"
        )
    return updated_notification


@router.patch(
    "/read-all",
    response_model=dict,
    summary="Marcar todas como leídas",
    description="Marca todas las notificaciones del usuario como leídas"
)
def mark_all_notifications_as_read(
    current_user: UserResponse = Depends(get_current_user),
    use_cases: NotificationUseCases = Depends(get_use_cases)
):
    updated_count = use_cases.mark_all_as_read(current_user.id)
    return {
        "message": f"Se marcaron {updated_count} notificaciones como leídas",
        "updated_count": updated_count
    }


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar notificación",
    description="Elimina una notificación del usuario"
)
def delete_notification(
    notification_id: int,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: NotificationUseCases = Depends(get_use_cases)
):
    deleted = use_cases.delete_notification(notification_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada"
        )


@router.delete(
    "/cleanup/old",
    response_model=dict,
    summary="Limpiar notificaciones antiguas",
    description="Elimina notificaciones leídas de más de 30 días"
)
def cleanup_old_notifications(
    days_old: int = Query(30, ge=1, le=365, description="Días de antigüedad"),
    current_user: UserResponse = Depends(get_current_user),
    use_cases: NotificationUseCases = Depends(get_use_cases)
):
    deleted_count = use_cases.clean_old_notifications(
        current_user.id, days_old)
    return {
        "message": f"Se eliminaron {deleted_count} notificaciones antiguas",
        "deleted_count": deleted_count,
        "days_old": days_old
    }
