"""
Repositorio para lecturas de sensores PIR desde InfluxDB
"""

from typing import List, Optional
from datetime import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi

from ..application.interfaces import LecturaPIRRepositoryInterface
from ..domain.entities import LecturaPIR
from ...core.db_influx import get_influx_client


class LecturaPIRRepository(LecturaPIRRepositoryInterface):
    """Implementación del repositorio de lecturas PIR usando InfluxDB"""

    def __init__(self):
        self._client: InfluxDBClient = get_influx_client()
        self._query_api: QueryApi = self._client.query_api()
        self._bucket = "sensores"  # Bucket donde están los datos
        self._measurement = "motion_sensor_metrics"  # Measurement para sensores PIR

    async def get_lecturas_by_time_range(
        self,
        time_range: str,
        mac_address: Optional[str] = None
    ) -> List[LecturaPIR]:
        """
        Obtiene lecturas PIR desde InfluxDB filtradas por rango de tiempo

        Args:
            time_range: Rango de tiempo (1m, 1h, 1d, 1w, 1mo, 1y)
            mac_address: Dirección MAC opcional para filtrar por sensor específico

        Returns:
            Lista de entidades LecturaPIR
        """
        try:
            # Construir filtro de MAC si se proporciona
            mac_filter = f'|> filter(fn: (r) => r["mac"] == "{mac_address}")' if mac_address else ""

            # Construir query Flux
            query = f'''
            from(bucket: "{self._bucket}")
                |> range(start: -{time_range})
                |> filter(fn: (r) => r["_measurement"] == "{self._measurement}")
                |> filter(fn: (r) => r["_field"] == "motion_detected")
                {mac_filter}
                |> sort(columns: ["_time"], desc: true)
                |> limit(n: 1000)
            '''

            # Ejecutar query
            tables = self._query_api.query(query=query)
            lecturas = []

            # Procesar resultados
            for table in tables:
                for record in table.records:
                    try:
                        # Convertir valor a boolean
                        motion_value = record.values.get("_value", False)
                        if isinstance(motion_value, str):
                            motion_detected = motion_value.lower() in [
                                'true', '1', 'yes']
                        else:
                            motion_detected = bool(motion_value)

                        lectura = LecturaPIR(
                            mac=record.values.get("mac", ""),
                            motion_detected=motion_detected,
                            timestamp=record.get_time()
                        )
                        lecturas.append(lectura)
                    except (ValueError, TypeError) as e:
                        # Log del error pero continuar procesando otros registros
                        print(f"Error procesando registro PIR: {e}")
                        continue

            return lecturas

        except Exception as e:
            raise Exception(
                f"Error consultando InfluxDB para sensores PIR: {str(e)}")
