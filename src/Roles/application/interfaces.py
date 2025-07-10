from abc import ABC, abstractmethod
from typing import List
from src.Roles.domain.schemas import RolCreate, RolUpdate, RolResponse


class RolRepositoryInterface(ABC):
    """Puerto que define qué operaciones debe implementar un repositorio"""

    @abstractmethod
    def get_all(self) -> List[RolResponse]:
        pass

    @abstractmethod
    def get_by_id(self, id_rol: int) -> RolResponse:
        pass

    @abstractmethod
    def create(self, rol: RolCreate) -> RolResponse:
        pass

    @abstractmethod
    def update(self, id_rol: int, rol: RolUpdate) -> RolResponse:
        pass

    @abstractmethod
    def delete(self, id_rol: int) -> None:
        pass
