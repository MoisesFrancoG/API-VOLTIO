from abc import ABC, abstractmethod
from typing import List
from src.Roles.domain.schemas import RoleCreate, RoleUpdate, RoleResponse


class RoleRepositoryInterface(ABC):
    """Puerto que define qué operaciones debe implementar un repositorio"""

    @abstractmethod
    def get_all(self) -> List[RoleResponse]:
        pass

    @abstractmethod
    def get_by_id(self, role_id: int) -> RoleResponse:
        pass

    @abstractmethod
    def create(self, role: RoleCreate) -> RoleResponse:
        pass

    @abstractmethod
    def update(self, role_id: int, role: RoleUpdate) -> RoleResponse:
        pass

    @abstractmethod
    def delete(self, role_id: int) -> None:
        pass
