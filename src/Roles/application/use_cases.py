from typing import List
from src.Roles.domain.schemas import RoleCreate, RoleUpdate, RoleResponse
from src.Roles.application.interfaces import RoleRepositoryInterface


class RoleUseCases:
    """Casos de uso para la entidad Role"""

    def __init__(self, repository: RoleRepositoryInterface):
        self.repository = repository

    def list_roles(self) -> List[RoleResponse]:
        return self.repository.get_all()

    def get_role(self, role_id: int) -> RoleResponse:
        return self.repository.get_by_id(role_id)

    def create_role(self, role: RoleCreate) -> RoleResponse:
        return self.repository.create(role)

    def update_role(self, role_id: int, role: RoleUpdate) -> RoleResponse:
        return self.repository.update(role_id, role)

    def delete_role(self, role_id: int) -> None:
        self.repository.delete(role_id)
