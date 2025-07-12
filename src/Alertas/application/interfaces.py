from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from src.Alertas.domain.schemas import AlertaCreate, AlertaUpdate, AlertaResponse


class AlertaRepositoryInterface(ABC):
    """Puerto que define qué operaciones debe implementar un repositorio"""

    @abstractmethod
    def get_all(self) -> List[AlertaResponse]:
        pass

    @abstractmethod
    def get_by_id(self, id_alerta: int) -> AlertaResponse:
        pass

    @abstractmethod
    def get_by_lectura(self, id_lectura: int) -> List[AlertaResponse]:
        pass

    @abstractmethod
    def get_by_tipo(self, tipo_alerta: str) -> List[AlertaResponse]:
        pass

    @abstractmethod
    def get_criticas(self) -> List[AlertaResponse]:
        pass

    @abstractmethod
    def get_recientes(self, horas: int = 24) -> List[AlertaResponse]:
        pass

    @abstractmethod
    def create(self, alerta: AlertaCreate) -> AlertaResponse:
        pass

    @abstractmethod
    def update(self, id_alerta: int, alerta: AlertaUpdate) -> AlertaResponse:
        pass

    @abstractmethod
    def delete(self, id_alerta: int) -> None:
        pass
