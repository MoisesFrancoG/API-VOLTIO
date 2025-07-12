"""
Rutas FastAPI para el módulo de Lecturas
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from ..application.use_cases import LecturaUseCases
from ..domain.schemas import LecturaCreate, LecturaUpdate, LecturaResponse
from .database import get_lectura_use_cases

router = APIRouter(prefix="/lecturas", tags=["lecturas"])

@router.post("/", response_model=LecturaResponse)
async def crear_lectura(
    lectura: LecturaCreate,
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """Crear una nueva lectura"""
    try:
        lectura_creada = await use_cases.crear_lectura(lectura)
        return LecturaResponse(
            id_lectura=lectura_creada.id_lectura,
            id_sensor=lectura_creada.id_sensor,
            valor=lectura_creada.valor,
            unidad=lectura_creada.unidad,
            fecha_hora=lectura_creada.fecha_hora
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/{id_lectura}", response_model=LecturaResponse)
async def obtener_lectura(
    id_lectura: int,
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """Obtener una lectura específica por ID"""
    try:
        lectura = await use_cases.obtener_lectura(id_lectura)
        if not lectura:
            raise HTTPException(status_code=404, detail="Lectura no encontrada")
        
        return LecturaResponse(
            id_lectura=lectura.id_lectura,
            id_sensor=lectura.id_sensor,
            valor=lectura.valor,
            unidad=lectura.unidad,
            fecha_hora=lectura.fecha_hora
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/", response_model=List[LecturaResponse])
async def obtener_todas_lecturas(
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """Obtener todas las lecturas"""
    try:
        lecturas = await use_cases.obtener_todas_lecturas()
        return [
            LecturaResponse(
                id_lectura=lectura.id_lectura,
                id_sensor=lectura.id_sensor,
                valor=lectura.valor,
                unidad=lectura.unidad,
                fecha_hora=lectura.fecha_hora
            )
            for lectura in lecturas
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/sensor/{id_sensor}", response_model=List[LecturaResponse])
async def obtener_lecturas_por_sensor(
    id_sensor: int,
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """Obtener todas las lecturas de un sensor específico"""
    try:
        lecturas = await use_cases.obtener_lecturas_por_sensor(id_sensor)
        return [
            LecturaResponse(
                id_lectura=lectura.id_lectura,
                id_sensor=lectura.id_sensor,
                valor=lectura.valor,
                unidad=lectura.unidad,
                fecha_hora=lectura.fecha_hora
            )
            for lectura in lecturas
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/sensor/{id_sensor}/ultimas", response_model=List[LecturaResponse])
async def obtener_ultimas_lecturas_por_sensor(
    id_sensor: int,
    limite: int = Query(10, ge=1, le=100, description="Número máximo de lecturas a retornar"),
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """Obtener las últimas N lecturas de un sensor específico"""
    try:
        lecturas = await use_cases.obtener_ultimas_lecturas_por_sensor(id_sensor, limite)
        return [
            LecturaResponse(
                id_lectura=lectura.id_lectura,
                id_sensor=lectura.id_sensor,
                valor=lectura.valor,
                unidad=lectura.unidad,
                fecha_hora=lectura.fecha_hora
            )
            for lectura in lecturas
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/rango-fechas/", response_model=List[LecturaResponse])
async def obtener_lecturas_por_rango_fechas(
    fecha_inicio: datetime = Query(..., description="Fecha de inicio (YYYY-MM-DD HH:MM:SS)"),
    fecha_fin: datetime = Query(..., description="Fecha de fin (YYYY-MM-DD HH:MM:SS)"),
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """Obtener lecturas dentro de un rango de fechas"""
    try:
        lecturas = await use_cases.obtener_lecturas_por_rango_fechas(fecha_inicio, fecha_fin)
        return [
            LecturaResponse(
                id_lectura=lectura.id_lectura,
                id_sensor=lectura.id_sensor,
                valor=lectura.valor,
                unidad=lectura.unidad,
                fecha_hora=lectura.fecha_hora
            )
            for lectura in lecturas
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/sensor/{id_sensor}/rango-fechas", response_model=List[LecturaResponse])
async def obtener_lecturas_por_sensor_y_fechas(
    id_sensor: int,
    fecha_inicio: datetime = Query(..., description="Fecha de inicio (YYYY-MM-DD HH:MM:SS)"),
    fecha_fin: datetime = Query(..., description="Fecha de fin (YYYY-MM-DD HH:MM:SS)"),
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """Obtener lecturas de un sensor específico dentro de un rango de fechas"""
    try:
        lecturas = await use_cases.obtener_lecturas_por_sensor_y_fechas(id_sensor, fecha_inicio, fecha_fin)
        return [
            LecturaResponse(
                id_lectura=lectura.id_lectura,
                id_sensor=lectura.id_sensor,
                valor=lectura.valor,
                unidad=lectura.unidad,
                fecha_hora=lectura.fecha_hora
            )
            for lectura in lecturas
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/criticas/", response_model=List[LecturaResponse])
async def obtener_lecturas_criticas(
    limite_superior: float = Query(100.0, description="Límite superior para valores críticos"),
    limite_inferior: float = Query(0.0, description="Límite inferior para valores críticos"),
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """Obtener lecturas que están fuera de los límites normales"""
    try:
        lecturas = await use_cases.obtener_lecturas_criticas(limite_superior, limite_inferior)
        return [
            LecturaResponse(
                id_lectura=lectura.id_lectura,
                id_sensor=lectura.id_sensor,
                valor=lectura.valor,
                unidad=lectura.unidad,
                fecha_hora=lectura.fecha_hora
            )
            for lectura in lecturas
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/sensor/{id_sensor}/estadisticas")
async def obtener_estadisticas_sensor(
    id_sensor: int,
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """Obtener estadísticas completas de un sensor"""
    try:
        estadisticas = await use_cases.obtener_estadisticas_sensor(id_sensor)
        return estadisticas
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/sensor/{id_sensor}/tendencia")
async def analizar_tendencia_sensor(
    id_sensor: int,
    limite_lecturas: int = Query(100, ge=10, le=1000, description="Número de lecturas para analizar"),
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """Analizar la tendencia de las lecturas de un sensor"""
    try:
        tendencia = await use_cases.analizar_tendencia_sensor(id_sensor, limite_lecturas)
        return tendencia
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put("/{id_lectura}", response_model=LecturaResponse)
async def actualizar_lectura(
    id_lectura: int,
    lectura: LecturaUpdate,
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """Actualizar una lectura existente"""
    try:
        lectura_actualizada = await use_cases.actualizar_lectura(id_lectura, lectura)
        if not lectura_actualizada:
            raise HTTPException(status_code=404, detail="Lectura no encontrada")
        
        return LecturaResponse(
            id_lectura=lectura_actualizada.id_lectura,
            id_sensor=lectura_actualizada.id_sensor,
            valor=lectura_actualizada.valor,
            unidad=lectura_actualizada.unidad,
            fecha_hora=lectura_actualizada.fecha_hora
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/{id_lectura}")
async def eliminar_lectura(
    id_lectura: int,
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """Eliminar una lectura"""
    try:
        eliminada = await use_cases.eliminar_lectura(id_lectura)
        if not eliminada:
            raise HTTPException(status_code=404, detail="Lectura no encontrada")
        
        return {"mensaje": "Lectura eliminada exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/sensor/{id_sensor}/contar")
async def contar_lecturas_por_sensor(
    id_sensor: int,
    use_cases: LecturaUseCases = Depends(get_lectura_use_cases)
):
    """Contar el número de lecturas de un sensor específico"""
    try:
        total = await use_cases.contar_lecturas_por_sensor(id_sensor)
        return {"id_sensor": id_sensor, "total_lecturas": total}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
