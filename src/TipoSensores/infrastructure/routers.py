"""
FastAPI routes for the DeviceTypes module
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.db import get_database
from src.core.auth_middleware import get_current_user, require_admin, require_admin_or_moderator
from src.Usuarios.domain.schemas import UserResponse
from src.TipoSensores.domain.schemas import DeviceTypeCreate, DeviceTypeUpdate, DeviceTypeResponse
from src.TipoSensores.application.use_cases import DeviceTypeUseCases
from src.TipoSensores.infrastructure.database import get_device_type_use_cases


router = APIRouter(prefix="/device-types", tags=["Device Types"])


def get_use_cases(db: Session = Depends(get_database)) -> DeviceTypeUseCases:
    """Dependency to get DeviceType use cases"""
    return get_device_type_use_cases(db)


@router.get(
    "/",
    response_model=List[DeviceTypeResponse],
    summary="List all device types",
    description="Gets a list of all device types (requires authentication)"
)
def list_device_types(
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceTypeUseCases = Depends(get_use_cases)
):
    """Get all device types (requires authentication)"""
    return use_cases.list_device_types()


@router.get(
    "/{device_type_id}",
    response_model=DeviceTypeResponse,
    summary="Get device type by ID",
    description="Gets a specific device type by its ID (requires authentication)"
)
def get_device_type(
    device_type_id: int,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: DeviceTypeUseCases = Depends(get_use_cases)
):
    """Get a device type by ID (requires authentication)"""
    return use_cases.get_device_type(device_type_id)


@router.post(
    "/",
    response_model=DeviceTypeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new device type",
    description="Creates a new device type in the system (requires admin permissions)"
)
def create_device_type(
    device_type: DeviceTypeCreate,
    current_user: UserResponse = Depends(require_admin()),
    use_cases: DeviceTypeUseCases = Depends(get_use_cases)
):
    """Create a new device type (requires admin only)"""
    return use_cases.create_device_type(device_type)


@router.put(
    "/{device_type_id}",
    response_model=DeviceTypeResponse,
    summary="Update device type",
    description="Updates an existing device type (requires admin permissions)"
)
def update_device_type(
    device_type_id: int,
    device_type: DeviceTypeUpdate,
    current_user: UserResponse = Depends(require_admin()),
    use_cases: DeviceTypeUseCases = Depends(get_use_cases)
):
    """Update an existing device type (requires admin or moderator)"""
    return use_cases.update_device_type(device_type_id, device_type)


@router.delete(
    "/{device_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete device type",
    description="Deletes a device type from the system (requires administrator permissions)"
)
def delete_device_type(
    device_type_id: int,
    current_user: UserResponse = Depends(require_admin()),
    use_cases: DeviceTypeUseCases = Depends(get_use_cases)
):
    """Delete a device type (requires admin)"""
    use_cases.delete_device_type(device_type_id)
    return {"message": "Device type deleted successfully"}
