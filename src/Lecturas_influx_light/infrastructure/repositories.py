"""
Repositorio para lecturas de sensores de luz desde InfluxDB
"""

from typing import List, Optional
from datetime import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi

from ..application.interfaces import LecturaLightRepositoryInterface
from ..domain.entities import LecturaLight
from ...core.db_influx import get_influx_client


class LecturaLightRepository(LecturaLightRepositoryInterface):
    """Implementación del repositorio de lecturas de luz usando InfluxDB"""

    def __init__(self):
        self._client: InfluxDBClient = get_influx_client()
        self._query_api: QueryApi = self._client.query_api()
        self._bucket = "sensores"  # Bucket donde están los datos
        self._measurement = "light_sensor_metrics"  # Measurement para sensores de luz

    async def get_lecturas_by_time_range(
        self,
        time_range: str,
        mac_address: Optional[str] = None
    ) -> List[LecturaLight]:
        """
        Obtiene lecturas de sensores de luz desde InfluxDB filtradas por rango de tiempo

        Args:
            time_range: Rango de tiempo (1m, 1h, 1d, 1w, 1mo, 1y)
            mac_address: Dirección MAC opcional para filtrar por sensor específico

        Returns:
            Lista de entidades LecturaLight
        """
        try:
            # Construir filtro de MAC si se proporciona
            mac_filter = f'|> filter(fn: (r) => r["mac"] == "{mac_address}")' if mac_address else ""

            # Construir query Flux
            query = f'''
            from(bucket: "{self._bucket}")
                |> range(start: -{time_range})
                |> filter(fn: (r) => r["_measurement"] == "{self._measurement}")
                |> filter(fn: (r) => r["_field"] == "light_level")
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
                        lectura = LecturaLight(
                            mac=record.values.get("mac", ""),
                            light_level=float(
                                record.values.get("_value", 0.0)),
                            timestamp=record.get_time()
                        )
                        lecturas.append(lectura)
                    except (ValueError, TypeError) as e:
                        # Log del error pero continuar procesando otros registros
                        print(
                            f"Error procesando registro de sensor de luz: {e}")
                        continue

            return lecturas

        except Exception as e:
            raise Exception(
                f"Error consultando InfluxDB para sensores de luz: {str(e)}")
