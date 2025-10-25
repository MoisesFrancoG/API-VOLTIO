"""
FastAPI routes for the DeviceCommand module
"""

from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from src.core.db import get_database
from src.core.auth_middleware import get_current_user, require_admin, require_admin_or_moderator
from src.Usuarios.domain.schemas import UsuarioResponse
from src.ComandosIR.domain.schemas import DeviceCommandCreate, DeviceCommandUpdate, DeviceCommandResponse
from src.ComandosIR.application.use_cases import DeviceCommandUseCases
from src.ComandosIR.infrastructure.database import get_device_command_use_cases


router = APIRouter(prefix="/device-commands", tags=["Device Commands"])


def get_use_cases(db: Session = Depends(get_database)) -> DeviceCommandUseCases:
    """Dependency to get DeviceCommand use cases"""
    return get_device_command_use_cases(db)


@router.get(
    "/",
    response_model=List[DeviceCommandResponse],
    summary="List all device commands",
    description="Get a list of all device commands (requires authentication)"
)
def list_device_commands(
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: DeviceCommandUseCases = Depends(get_use_cases)
):
    """Get all device commands (requires authentication)"""
    return use_cases.list_device_commands()


@router.get(
    "/device/{device_id}",
    response_model=List[DeviceCommandResponse],
    summary="List device commands by device",
    description="Get all device commands for a specific device (requires authentication)"
)
def list_commands_by_device(
    device_id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: DeviceCommandUseCases = Depends(get_use_cases)
):
    """Get all device commands for a specific device (requires authentication)"""
    return use_cases.get_commands_by_device(device_id)


@router.get(
    "/{id}",
    response_model=DeviceCommandResponse,
    summary="Get device command by ID",
    description="Get a specific device command by its ID (requires authentication)"
)
def get_device_command(
    id: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: DeviceCommandUseCases = Depends(get_use_cases)
):
    """Get a specific device command by ID (requires authentication)"""
    return use_cases.get_device_command(id)


@router.post(
    "/",
    response_model=DeviceCommandResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create device command",
    description="Create a new device command (requires admin or moderator permissions)"
)
def create_device_command(
    device_command: DeviceCommandCreate,
    current_user: UsuarioResponse = Depends(require_admin_or_moderator),
    use_cases: DeviceCommandUseCases = Depends(get_use_cases)
):
    """Create a new device command (requires admin or moderator permissions)"""
    return use_cases.create_device_command(device_command)


@router.put(
    "/{id}",
    response_model=DeviceCommandResponse,
    summary="Update device command",
    description="Update an existing device command (requires admin or moderator permissions)"
)
def update_device_command(
    id: int,
    device_command: DeviceCommandUpdate,
    current_user: UsuarioResponse = Depends(require_admin_or_moderator),
    use_cases: DeviceCommandUseCases = Depends(get_use_cases)
):
    """Update an existing device command (requires admin or moderator permissions)"""
    return use_cases.update_device_command(id, device_command)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete device command",
    description="Delete a device command (requires admin permissions)"
)
def delete_device_command(
    id: int,
    current_user: UsuarioResponse = Depends(require_admin),
    use_cases: DeviceCommandUseCases = Depends(get_use_cases)
):
    """Delete a device command (requires admin permissions)"""
    use_cases.delete_device_command(id)
