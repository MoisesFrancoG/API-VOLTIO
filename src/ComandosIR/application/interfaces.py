from abc import ABC, abstractmethod
from typing import List
from src.ComandosIR.domain.schemas import ComandoIRCreate, ComandoIRUpdate, ComandoIRResponse


class ComandoIRRepositoryInterface(ABC):
    """Puerto que define qué operaciones debe implementar un repositorio"""

    @abstractmethod
    def get_all(self) -> List[ComandoIRResponse]:
        pass

    @abstractmethod
    def get_by_id(self, id_comando: int) -> ComandoIRResponse:
        pass

    @abstractmethod
    def get_by_sensor(self, id_sensor: int) -> List[ComandoIRResponse]:
        pass

    @abstractmethod
    def create(self, comando_ir: ComandoIRCreate) -> ComandoIRResponse:
        pass

    @abstractmethod
    def update(self, id_comando: int, comando_ir: ComandoIRUpdate) -> ComandoIRResponse:
        pass

    @abstractmethod
    def delete(self, id_comando: int) -> None:
        pass
