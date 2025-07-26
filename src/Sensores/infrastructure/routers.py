

from .database import get_device_use_cases
from src.Usuarios.domain.schemas import UserResponse
from src.core.rabbitmq import publish_ir_command, publish_relay_command
from src.core.auth_middleware import get_current_user
from ..domain.schemas import (
    DeviceCreate, DeviceUpdate, DeviceResponse, DeviceBase,
    DeviceStatusUpdate, RelayCommandRequest, RelayCommandResponse
)
from ..application.use_cases import DeviceUseCases
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status


"""
FastAPI routes for the Devices module
"""


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(
    device: DeviceCreate,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Create a new device for the authenticated user"""
    try:
        # Crear un objeto similar a DeviceBase con todos los campos necesarios
        class DeviceWithUser:
            def __init__(self, device_create, user_id):
                self.name = device_create.name
                self.device_type_id = device_create.device_type_id
                self.user_id = user_id  # ✅ Tomado automáticamente del token
                self.is_active = device_create.is_active
                self.mac_address = device_create.mac_address
                self.description = device_create.description

        device_with_user = DeviceWithUser(device, current_user.id)

        created_device = use_cases.create_device(device_with_user)
        return DeviceResponse(
            id=created_device.id,
            name=created_device.name,
            device_type_id=created_device.device_type_id,
            user_id=created_device.user_id,
            is_active=created_device.is_active,
            mac_address=getattr(created_device, 'mac_address', None),
            description=getattr(created_device, 'description', None),
            created_at=getattr(created_device, 'created_at', None)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/me", response_model=List[DeviceResponse], summary="Get my devices", description="Devuelve los dispositivos del usuario autenticado.")
def get_my_devices(
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Devuelve los dispositivos asociados al usuario autenticado."""
    try:
        devices = use_cases.get_devices_by_user(current_user.id)
        return [
            DeviceResponse(
                id=device.id,
                name=device.name,
                device_type_id=device.device_type_id,
                user_id=device.user_id,
                is_active=device.is_active,
                mac_address=getattr(device, 'mac_address', None),
                description=getattr(device, 'description', None),
                created_at=getattr(device, 'created_at', None)
            )
            for device in devices
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: int,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Get a specific device by ID (requires authentication)"""
    try:
        device = use_cases.get_device(device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")

        return DeviceResponse(
            id=device.id,
            name=device.name,
            device_type_id=device.device_type_id,
            user_id=device.user_id,
            is_active=device.is_active,
            mac_address=getattr(device, 'mac_address', None),
            description=getattr(device, 'description', None),
            created_at=getattr(device, 'created_at', None)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/", response_model=List[DeviceResponse])
def get_all_devices(
    active_only: Optional[bool] = Query(
        None, description="Filter by active status"),
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Get all devices or only active devices (requires authentication)"""
    try:
        if active_only is True:
            devices = use_cases.get_active_devices()
        else:
            devices = use_cases.get_all_devices()

        return [
            DeviceResponse(
                id=device.id,
                name=device.name,
                device_type_id=device.device_type_id,
                user_id=device.user_id,
                is_active=device.is_active,
                mac_address=getattr(device, 'mac_address', None),
                description=getattr(device, 'description', None),
                created_at=getattr(device, 'created_at', None)
            )
            for device in devices
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/type/{device_type_id}", response_model=List[DeviceResponse])
def get_devices_by_type(
    device_type_id: int,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Get devices by type (requires authentication)"""
    try:
        devices = use_cases.get_devices_by_type(device_type_id)
        return [
            DeviceResponse(
                id=device.id,
                name=device.name,
                device_type_id=device.device_type_id,
                user_id=device.user_id,
                is_active=device.is_active
            )
            for device in devices
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/location/{location_id}", response_model=List[DeviceResponse])
def get_devices_by_location(
    location_id: int,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Get devices by location (requires authentication)"""
    try:
        devices = use_cases.get_devices_by_location(location_id)
        return [
            DeviceResponse(
                id=device.id,
                name=device.name,
                device_type_id=device.device_type_id,
                user_id=device.user_id,
                is_active=device.is_active
            )
            for device in devices
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/user/{user_id}", response_model=List[DeviceResponse])
def get_devices_by_user(
    user_id: int,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Get devices by user (requires authentication)"""
    try:
        devices = use_cases.get_devices_by_user(user_id)
        return [
            DeviceResponse(
                id=device.id,
                name=device.name,
                device_type_id=device.device_type_id,
                user_id=device.user_id,
                is_active=device.is_active
            )
            for device in devices
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/search/", response_model=List[DeviceResponse])
def search_devices_by_name(
    name: str = Query(..., min_length=2, description="Search term"),
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Search devices by name (requires authentication)"""
    try:
        devices = use_cases.search_devices_by_name(name)
        return [
            DeviceResponse(
                id=device.id,
                name=device.name,
                device_type_id=device.device_type_id,
                user_id=device.user_id,
                is_active=device.is_active,
                mac_address=getattr(device, 'mac_address', None),
                description=getattr(device, 'description', None),
                created_at=getattr(device, 'created_at', None)
            )
            for device in devices
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: int,
    device: DeviceUpdate,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Update an existing device (requires authentication)"""
    try:
        updated_device = use_cases.update_device(device_id, device)
        if not updated_device:
            raise HTTPException(status_code=404, detail="Device not found")

        return DeviceResponse(
            id=updated_device.id,
            name=updated_device.name,
            device_type_id=updated_device.device_type_id,
            location_id=updated_device.location_id,
            user_id=updated_device.user_id,
            is_active=updated_device.is_active,
            mac_address=getattr(updated_device, 'mac_address', None),
            description=getattr(updated_device, 'description', None),
            created_at=getattr(updated_device, 'created_at', None)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/{device_id}/status", response_model=DeviceResponse)
def change_device_status(
    device_id: int,
    status: DeviceStatusUpdate,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Change only the active/inactive status of the device (requires authentication)"""
    try:
        updated_device = use_cases.change_device_status(
            device_id, status.is_active)
        if not updated_device:
            raise HTTPException(status_code=404, detail="Device not found")

        return DeviceResponse(
            id=updated_device.id,
            name=updated_device.name,
            device_type_id=updated_device.device_type_id,
            location_id=updated_device.location_id,
            user_id=updated_device.user_id,
            is_active=updated_device.is_active
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{device_id}")
def delete_device(
    device_id: int,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Delete a device (requires authentication)"""
    try:
        deleted = use_cases.delete_device(device_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Device not found")

        return {"message": "Device deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


# ===============================================================================
# RELAY COMMAND ENDPOINT - Control de relé para dispositivos NODO_CONTROL_PZEM
# ===============================================================================

@router.post("/{mac_address}/command/relay",
             response_model=RelayCommandResponse,
             status_code=status.HTTP_202_ACCEPTED,
             summary="Send relay command to device",
             description="Sends ON/OFF command to relay of a NODO_CONTROL_PZEM device")
def send_relay_command(
    mac_address: str,
    command: RelayCommandRequest,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """
    Send relay command to a specific device

    - **mac_address**: MAC address of the target device
    - **action**: Command to send ("ON" or "OFF")

    Only works with NODO_CONTROL_PZEM devices owned by the authenticated user.
    """
    try:
        # FASE 1: VALIDACIÓN Y SEGURIDAD
        logger.info(
            f"🔍 User {current_user.id} requesting relay command '{command.action}' for device {mac_address}")

        # FASE 2: VERIFICACIÓN DE LÓGICA DE NEGOCIO
        validation_result = use_cases.validate_relay_command_permissions(
            mac_address=mac_address,
            user_id=current_user.id
        )

        device = validation_result['device']
        logger.info(
            f"✅ Validation passed - Device: {device.name} (Type: {validation_result['type_name']})")

        # FASE 3: PUBLICACIÓN EN RABBITMQ
        success = publish_relay_command(mac_address, command.action)
        print(command.action)

        if not success:
            logger.error(
                f"❌ Failed to publish command to RabbitMQ for device {mac_address}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )

        # FASE 4: RESPUESTA DE ÉXITO
        logger.info(
            f"✅ Relay command '{command.action}' sent successfully to device {mac_address}")

        return RelayCommandResponse(
            status="Comando de relé enviado al dispositivo",
            device_mac=mac_address,
            action_sent=command.action
        )

    except ValueError as e:
        error_message = str(e)
        logger.warning(
            f"⚠️ Validation error for device {mac_address}: {error_message}")

        # Map specific validation errors to appropriate HTTP status codes
        if "not found" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dispositivo no encontrado"
            )
        elif "access denied" in error_message.lower() or "not owned" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado"
            )
        elif "operation not allowed" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "Operación no permitida",
                    "detail": "Este comando solo es aplicable a dispositivos de tipo 'NODO_CONTROL_PZEM'"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Petición inválida"
            )

    except Exception as e:
        logger.error(f"❌ Unexpected error in relay command endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/{mac_address}/command/ir",
             response_model=RelayCommandResponse,
             status_code=status.HTTP_202_ACCEPTED,
             summary="Send IR command to device",
             description="Sends ON/OFF command to IR of a NODO_CONTROL_IR device")
def send_ir_command(
    mac_address: str,
    command: RelayCommandRequest,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """
    Send IR command to a specific device

    - **mac_address**: MAC address of the target device
    - **action**: Command to send (e.g., "ON" or "OFF")

    Only works with NODO_CONTROL_IR devices owned by the authenticated user.
    """
    try:
        # FASE 1: VALIDACIÓN Y SEGURIDAD
        logger.info(
            f"🔍 User {current_user.id} requesting IR command '{command.action}' for device {mac_address}")

        # FASE 2: VERIFICACIÓN DE LÓGICA DE NEGOCIO
        validation_result = use_cases.validate_ir_command_permissions(
            mac_address=mac_address,
            user_id=current_user.id
        )

        device = validation_result['device']
        logger.info(
            f"✅ Validation passed - Device: {device.name} (Type: {validation_result['type_name']})")

        # FASE 3: PUBLICACIÓN EN RABBITMQ (topic ir/command/{MAC})
        topic = f"ir/command/{mac_address}"
        # Remove colons from mac_address before publishing
        mac_no_colon = mac_address.replace(":", "")
        success = publish_ir_command(mac_no_colon, command.action)
        print(command.action)

        if not success:
            logger.error(
                f"❌ Failed to publish IR command to RabbitMQ for device {mac_address}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )

        # FASE 4: RESPUESTA DE ÉXITO
        logger.info(
            f"✅ IR command '{command.action}' sent successfully to device {mac_address}")

        return RelayCommandResponse(
            status="Comando IR enviado al dispositivo",
            device_mac=mac_address,
            action_sent=command.action
        )

    except ValueError as e:
        error_message = str(e)
        logger.warning(
            f"⚠️ Validation error for device {mac_address}: {error_message}")

        # Map specific validation errors to appropriate HTTP status codes
        if "not found" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dispositivo no encontrado"
            )
        elif "access denied" in error_message.lower() or "not owned" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado"
            )
        elif "operation not allowed" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "Operación no permitida",
                    "detail": "Este comando solo es aplicable a dispositivos de tipo 'NODO_CONTROL_IR'"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Petición inválida"
            )

    except Exception as e:
        logger.error(f"❌ Unexpected error in IR command endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
