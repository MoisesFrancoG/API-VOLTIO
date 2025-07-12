"""
Rutas FastAPI para el módulo de Sensores
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from ..application.use_cases import SensorUseCases
from ..domain.schemas import SensorCreate, SensorUpdate, SensorResponse, SensorEstadoUpdate
from .database import get_sensor_use_cases

router = APIRouter(prefix="/sensores", tags=["sensores"])

@router.post("/", response_model=SensorResponse)
def crear_sensor(
    sensor: SensorCreate,
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Crear un nuevo sensor"""
    try:
        sensor_creado = use_cases.crear_sensor(sensor)
        return SensorResponse(
            id_sensor=sensor_creado.id_sensor,
            nombre=sensor_creado.nombre,
            id_tipo_sensor=sensor_creado.id_tipo_sensor,
            id_ubicacion=sensor_creado.id_ubicacion,
            id_usuario=sensor_creado.id_usuario,
            activo=sensor_creado.activo
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/{id_sensor}", response_model=SensorResponse)
def obtener_sensor(
    id_sensor: int,
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Obtener un sensor específico por ID"""
    try:
        sensor = use_cases.obtener_sensor(id_sensor)
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        
        return SensorResponse(
            id_sensor=sensor.id_sensor,
            nombre=sensor.nombre,
            id_tipo_sensor=sensor.id_tipo_sensor,
            id_ubicacion=sensor.id_ubicacion,
            id_usuario=sensor.id_usuario,
            activo=sensor.activo
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/", response_model=List[SensorResponse])
def obtener_todos_sensores(
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Obtener todos los sensores"""
    try:
        sensores = use_cases.obtener_todos_sensores()
        return [
            SensorResponse(
                id_sensor=sensor.id_sensor,
                nombre=sensor.nombre,
                id_tipo_sensor=sensor.id_tipo_sensor,
                id_ubicacion=sensor.id_ubicacion,
                id_usuario=sensor.id_usuario,
                activo=sensor.activo
            )
            for sensor in sensores
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/activos/", response_model=List[SensorResponse])
def obtener_sensores_activos(
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Obtener solo los sensores activos"""
    try:
        sensores = use_cases.obtener_sensores_activos()
        return [
            SensorResponse(
                id_sensor=sensor.id_sensor,
                nombre=sensor.nombre,
                id_tipo_sensor=sensor.id_tipo_sensor,
                id_ubicacion=sensor.id_ubicacion,
                id_usuario=sensor.id_usuario,
                activo=sensor.activo
            )
            for sensor in sensores
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/tipo/{id_tipo_sensor}", response_model=List[SensorResponse])
def obtener_sensores_por_tipo(
    id_tipo_sensor: int,
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Obtener sensores por tipo"""
    try:
        sensores = use_cases.obtener_sensores_por_tipo(id_tipo_sensor)
        return [
            SensorResponse(
                id_sensor=sensor.id_sensor,
                nombre=sensor.nombre,
                id_tipo_sensor=sensor.id_tipo_sensor,
                id_ubicacion=sensor.id_ubicacion,
                id_usuario=sensor.id_usuario,
                activo=sensor.activo
            )
            for sensor in sensores
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/ubicacion/{id_ubicacion}", response_model=List[SensorResponse])
def obtener_sensores_por_ubicacion(
    id_ubicacion: int,
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Obtener sensores por ubicación"""
    try:
        sensores = use_cases.obtener_sensores_por_ubicacion(id_ubicacion)
        return [
            SensorResponse(
                id_sensor=sensor.id_sensor,
                nombre=sensor.nombre,
                id_tipo_sensor=sensor.id_tipo_sensor,
                id_ubicacion=sensor.id_ubicacion,
                id_usuario=sensor.id_usuario,
                activo=sensor.activo
            )
            for sensor in sensores
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/usuario/{id_usuario}", response_model=List[SensorResponse])
def obtener_sensores_por_usuario(
    id_usuario: int,
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Obtener sensores por usuario"""
    try:
        sensores = use_cases.obtener_sensores_por_usuario(id_usuario)
        return [
            SensorResponse(
                id_sensor=sensor.id_sensor,
                nombre=sensor.nombre,
                id_tipo_sensor=sensor.id_tipo_sensor,
                id_ubicacion=sensor.id_ubicacion,
                id_usuario=sensor.id_usuario,
                activo=sensor.activo
            )
            for sensor in sensores
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/buscar/", response_model=List[SensorResponse])
def buscar_sensores_por_nombre(
    nombre: str = Query(..., min_length=2, description="Término de búsqueda"),
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Buscar sensores por nombre"""
    try:
        sensores = use_cases.buscar_sensores_por_nombre(nombre)
        return [
            SensorResponse(
                id_sensor=sensor.id_sensor,
                nombre=sensor.nombre,
                id_tipo_sensor=sensor.id_tipo_sensor,
                id_ubicacion=sensor.id_ubicacion,
                id_usuario=sensor.id_usuario,
                activo=sensor.activo
            )
            for sensor in sensores
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/tipo/{id_tipo_sensor}/estadisticas")
def obtener_estadisticas_por_tipo(
    id_tipo_sensor: int,
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Obtener estadísticas de sensores por tipo"""
    try:
        estadisticas = use_cases.obtener_estadisticas_por_tipo(id_tipo_sensor)
        return estadisticas
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/ubicacion/{id_ubicacion}/estadisticas")
def obtener_estadisticas_por_ubicacion(
    id_ubicacion: int,
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Obtener estadísticas de sensores por ubicación"""
    try:
        estadisticas = use_cases.obtener_estadisticas_por_ubicacion(id_ubicacion)
        return estadisticas
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/usuario/{id_usuario}/estadisticas")
def obtener_estadisticas_por_usuario(
    id_usuario: int,
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Obtener estadísticas de sensores por usuario"""
    try:
        estadisticas = use_cases.obtener_estadisticas_por_usuario(id_usuario)
        return estadisticas
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/{id_sensor}/validar")
def validar_configuracion_sensor(
    id_sensor: int,
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Validar la configuración de un sensor"""
    try:
        validacion = use_cases.validar_configuracion_sensor(id_sensor)
        return validacion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put("/{id_sensor}", response_model=SensorResponse)
def actualizar_sensor(
    id_sensor: int,
    sensor: SensorUpdate,
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Actualizar un sensor existente"""
    try:
        sensor_actualizado = use_cases.actualizar_sensor(id_sensor, sensor)
        if not sensor_actualizado:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        
        return SensorResponse(
            id_sensor=sensor_actualizado.id_sensor,
            nombre=sensor_actualizado.nombre,
            id_tipo_sensor=sensor_actualizado.id_tipo_sensor,
            id_ubicacion=sensor_actualizado.id_ubicacion,
            id_usuario=sensor_actualizado.id_usuario,
            activo=sensor_actualizado.activo
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.patch("/{id_sensor}/estado", response_model=SensorResponse)
def cambiar_estado_sensor(
    id_sensor: int,
    estado: SensorEstadoUpdate,
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Cambiar solo el estado activo/inactivo del sensor"""
    try:
        sensor_actualizado = use_cases.cambiar_estado_sensor(id_sensor, estado.activo)
        if not sensor_actualizado:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        
        return SensorResponse(
            id_sensor=sensor_actualizado.id_sensor,
            nombre=sensor_actualizado.nombre,
            id_tipo_sensor=sensor_actualizado.id_tipo_sensor,
            id_ubicacion=sensor_actualizado.id_ubicacion,
            id_usuario=sensor_actualizado.id_usuario,
            activo=sensor_actualizado.activo
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/{id_sensor}")
def eliminar_sensor(
    id_sensor: int,
    use_cases: SensorUseCases = Depends(get_sensor_use_cases)
):
    """Eliminar un sensor"""
    try:
        eliminado = use_cases.eliminar_sensor(id_sensor)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        
        return {"mensaje": "Sensor eliminado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
