"""
Repositorio para lecturas DHT22 desde InfluxDB
"""

from typing import List, Optional
from datetime import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi

from ..application.interfaces import LecturaDHT22RepositoryInterface
from ..domain.entities import LecturaDHT22
from ...core.db_influx import get_influx_client


class LecturaDHT22Repository(LecturaDHT22RepositoryInterface):
    """Implementación del repositorio de lecturas DHT22 usando InfluxDB"""

    def __init__(self):
        self._client: InfluxDBClient = get_influx_client()
        self._query_api: QueryApi = self._client.query_api()
        self._bucket = "sensores"  # Bucket donde están los datos
        self._measurement = "temperature_humidity_metrics"  # Measurement para DHT22

    async def get_lecturas_by_time_range(
        self,
        time_range: str,
        mac_address: Optional[str] = None
    ) -> List[LecturaDHT22]:
        """
        Obtiene lecturas DHT22 desde InfluxDB filtradas por rango de tiempo

        Args:
            time_range: Rango de tiempo (1m, 1h, 1d, 1w, 1mo, 1y)
            mac_address: Dirección MAC opcional para filtrar por sensor específico

        Returns:
            Lista de entidades LecturaDHT22
        """
        try:
            # Construir filtro de MAC si se proporciona
            mac_filter = f'|> filter(fn: (r) => r["mac"] == "{mac_address}")' if mac_address else ""

            # Construir query Flux
            query = f'''
            from(bucket: "{self._bucket}")
                |> range(start: -{time_range})
                |> filter(fn: (r) => r["_measurement"] == "{self._measurement}")
                |> filter(fn: (r) => r["_field"] == "temperature" or r["_field"] == "humidity")
                {mac_filter}
                |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
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
                        lectura = LecturaDHT22(
                            mac=record.values.get("mac", ""),
                            temperature=float(
                                record.values.get("temperature", 0.0)),
                            humidity=float(record.values.get("humidity", 0.0)),
                            timestamp=record.get_time()
                        )
                        lecturas.append(lectura)
                    except (ValueError, TypeError) as e:
                        # Log del error pero continuar procesando otros registros
                        print(f"Error procesando registro DHT22: {e}")
                        continue

            return lecturas

        except Exception as e:
            raise Exception(f"Error consultando InfluxDB para DHT22: {str(e)}")
