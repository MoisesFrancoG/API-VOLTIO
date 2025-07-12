from typing import List
from src.TipoSensores.domain.schemas import TipoSensorCreate, TipoSensorUpdate, TipoSensorResponse
from src.TipoSensores.application.interfaces import TipoSensorRepositoryInterface


class TipoSensorUseCases:
    """Casos de uso para la entidad TipoSensor"""

    def __init__(self, repository: TipoSensorRepositoryInterface):
        self.repository = repository

    def listar_tipos_sensores(self) -> List[TipoSensorResponse]:
        return self.repository.get_all()

    def obtener_tipo_sensor(self, id_tipo_sensor: int) -> TipoSensorResponse:
        return self.repository.get_by_id(id_tipo_sensor)

    def crear_tipo_sensor(self, tipo_sensor: TipoSensorCreate) -> TipoSensorResponse:
        return self.repository.create(tipo_sensor)

    def actualizar_tipo_sensor(self, id_tipo_sensor: int, tipo_sensor: TipoSensorUpdate) -> TipoSensorResponse:
        return self.repository.update(id_tipo_sensor, tipo_sensor)

    def eliminar_tipo_sensor(self, id_tipo_sensor: int) -> None:
        self.repository.delete(id_tipo_sensor)
