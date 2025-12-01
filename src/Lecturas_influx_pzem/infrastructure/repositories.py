# Contenido COMPLETO y CORREGIDO del archivo

from typing import List
from fastapi import HTTPException, status
from influxdb_client.client.exceptions import InfluxDBError

from src.Lecturas_influx_pzem.application.interfaces import LecturaRepositoryInterface
from src.Lecturas_influx_pzem.domain.schemas import LecturaPZEMResponse, TimeRange
from src.core.db_influx import get_influx_query_api, INFLUX_BUCKET


class InfluxDBLecturaRepository(LecturaRepositoryInterface):
    """Implementación del repositorio usando el cliente de InfluxDB."""

    def __init__(self):
        self.query_api = get_influx_query_api()

    def get_by_time_range(
        self,
        time_range: TimeRange,
        mac: str | None = None,
        device_id: str | None = None
    ) -> List[LecturaPZEMResponse]:

        # Construcción de la consulta Flux
        flux_query = f'''
        from(bucket: "{INFLUX_BUCKET}")
          |> range(start: -{time_range.value})
          |> filter(fn: (r) => r["_measurement"] == "energy_metrics")
        '''

        # Añadimos el filtro por MAC si se proporciona (verificar si es tag o field)
        if mac:
            flux_query += f'\n  |> filter(fn: (r) => r["mac"] == "{mac}")'

        # Añadimos el filtro por deviceId si se proporciona
        if device_id:
            flux_query += f'\n  |> filter(fn: (r) => r["deviceId"] == "{device_id}")'

        # Pivotamos para tener los campos como columnas
        flux_query += '\n  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
        flux_query += '\n  |> sort(columns: ["_time"], desc: true)'
        flux_query += '\n  |> limit(n: 1000)'

        # Log de debugging
        print(f"[DEBUG] Flux Query: {flux_query}")
        print(f"[DEBUG] MAC filter: {mac}")
        print(f"[DEBUG] Device ID filter: {device_id}")

        try:
            tables = self.query_api.query(flux_query)

            # Mapeamos los resultados a nuestro esquema Pydantic
            results = []
            for table in tables:
                print(f"[DEBUG] Processing table with {len(table.records)} records")
                for record in table.records:
                    try:
                        # Preparamos los datos para el modelo
                        data = record.values.copy()
                        
                        # Log de datos recibidos
                        print(f"[DEBUG] Record values: {data}")

                        # Si no hay deviceId, usamos el mac como deviceId
                        if 'deviceId' not in data and 'mac' in data:
                            data['deviceId'] = data['mac']

                        # Validamos y agregamos el resultado
                        lectura = LecturaPZEMResponse.model_validate(data)
                        results.append(lectura)
                    except Exception as validation_error:
                        # Log del error para debugging
                        print(f"[ERROR] Error validando datos: {validation_error}")
                        print(f"[ERROR] Datos recibidos: {record.values}")
                        continue  # Saltamos este registro y continuamos con el siguiente

            print(f"[DEBUG] Total results: {len(results)}")
            return results
        except InfluxDBError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al consultar InfluxDB: {e}"
            )
