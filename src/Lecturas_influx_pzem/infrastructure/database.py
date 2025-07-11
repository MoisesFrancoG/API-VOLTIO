from src.Lecturas_influx_pzem.application.use_cases import LecturaUseCases
from src.Lecturas_influx_pzem.infrastructure.repositories import InfluxDBLecturaRepository

def get_lectura_repository() -> InfluxDBLecturaRepository:
    """Factory para crear instancia del repositorio de Lecturas."""
    return InfluxDBLecturaRepository()

def get_lectura_use_cases() -> LecturaUseCases:
    """Factory para crear instancia de los casos de uso de Lecturas."""
    repository = get_lectura_repository()
    return LecturaUseCases(repository)