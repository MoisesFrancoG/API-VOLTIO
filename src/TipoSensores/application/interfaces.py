from abc import ABC, abstractmethod
from typing import List
from src.TipoSensores.domain.schemas import TipoSensorCreate, TipoSensorUpdate, TipoSensorResponse


class TipoSensorRepositoryInterface(ABC):
    """Puerto que define qué operaciones debe implementar un repositorio"""

    @abstractmethod
    def get_all(self) -> List[TipoSensorResponse]:
        pass

    @abstractmethod
    def get_by_id(self, id_tipo_sensor: int) -> TipoSensorResponse:
        pass

    @abstractmethod
    def create(self, tipo_sensor: TipoSensorCreate) -> TipoSensorResponse:
        pass

    @abstractmethod
    def update(self, id_tipo_sensor: int, tipo_sensor: TipoSensorUpdate) -> TipoSensorResponse:
        pass

    @abstractmethod
    def delete(self, id_tipo_sensor: int) -> None:
        pass
