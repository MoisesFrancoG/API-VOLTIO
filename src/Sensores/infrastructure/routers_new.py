"""
FastAPI routes for the Devices module
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from ..application.use_cases import DeviceUseCases
from ..domain.schemas import DeviceCreate, DeviceUpdate, DeviceResponse, DeviceStatusUpdate
from .database import get_device_use_cases

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/", response_model=DeviceResponse)
def create_device(
    device: DeviceCreate,
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Create a new device"""
    try:
        created_device = use_cases.create_device(device)
        return DeviceResponse(
            id=created_device.id,
            name=created_device.name,
            device_type_id=created_device.device_type_id,
            location_id=created_device.location_id,
            user_id=created_device.user_id,
            active=created_device.active
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: int,
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Get a specific device by ID"""
    try:
        device = use_cases.get_device(device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")

        return DeviceResponse(
            id=device.id,
            name=device.name,
            device_type_id=device.device_type_id,
            location_id=device.location_id,
            user_id=device.user_id,
            active=device.active
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
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Get all devices or only active devices"""
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
                location_id=device.location_id,
                user_id=device.user_id,
                active=device.active
            )
            for device in devices
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/type/{device_type_id}", response_model=List[DeviceResponse])
def get_devices_by_type(
    device_type_id: int,
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Get devices by type"""
    try:
        devices = use_cases.get_devices_by_type(device_type_id)
        return [
            DeviceResponse(
                id=device.id,
                name=device.name,
                device_type_id=device.device_type_id,
                location_id=device.location_id,
                user_id=device.user_id,
                active=device.active
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
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Get devices by location"""
    try:
        devices = use_cases.get_devices_by_location(location_id)
        return [
            DeviceResponse(
                id=device.id,
                name=device.name,
                device_type_id=device.device_type_id,
                location_id=device.location_id,
                user_id=device.user_id,
                active=device.active
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
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Get devices by user"""
    try:
        devices = use_cases.get_devices_by_user(user_id)
        return [
            DeviceResponse(
                id=device.id,
                name=device.name,
                device_type_id=device.device_type_id,
                location_id=device.location_id,
                user_id=device.user_id,
                active=device.active
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
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Search devices by name"""
    try:
        devices = use_cases.search_devices_by_name(name)
        return [
            DeviceResponse(
                id=device.id,
                name=device.name,
                device_type_id=device.device_type_id,
                location_id=device.location_id,
                user_id=device.user_id,
                active=device.active
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
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Update an existing device"""
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
            active=updated_device.active
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
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Change only the active/inactive status of the device"""
    try:
        updated_device = use_cases.change_device_status(
            device_id, status.active)
        if not updated_device:
            raise HTTPException(status_code=404, detail="Device not found")

        return DeviceResponse(
            id=updated_device.id,
            name=updated_device.name,
            device_type_id=updated_device.device_type_id,
            location_id=updated_device.location_id,
            user_id=updated_device.user_id,
            active=updated_device.active
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
    use_cases: DeviceUseCases = Depends(get_device_use_cases)
):
    """Delete a device"""
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
