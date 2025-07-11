from influxdb_client import InfluxDBClient
from .config import settings # Asumo que añadirás la config de influx a tu config.py

# --- CONFIGURACIÓN DE INFLUXDB (Obtenida de tu archivo de settings) ---
INFLUX_URL = settings.INFLUX_URL
INFLUX_TOKEN = settings.INFLUX_TOKEN
INFLUX_ORG = settings.INFLUX_ORG
INFLUX_BUCKET = settings.INFLUX_BUCKET

# --- CLIENTE SINGLETON ---
# Creamos una única instancia del cliente para ser reutilizada en toda la app
# y evitar abrir conexiones constantemente.
_influx_client = None

def get_influx_client():
    global _influx_client
    if _influx_client is None:
        _influx_client = InfluxDBClient(
            url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG
        )
        print("Cliente de InfluxDB inicializado.")
    return _influx_client

def get_influx_query_api():
    """Dependencia para obtener el API de consulta."""
    client = get_influx_client()
    return client.query_api()

def close_influx_client():
    """Función para cerrar el cliente al apagar la app."""
    global _influx_client
    if _influx_client:
        _influx_client.close()
        print("Cliente de InfluxDB cerrado.")