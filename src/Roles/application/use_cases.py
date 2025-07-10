from typing import List
from src.Roles.domain.schemas import RolCreate, RolUpdate, RolResponse
from src.Roles.application.interfaces import RolRepositoryInterface


class RolUseCases:
    """Casos de uso para la entidad Rol"""

    def __init__(self, repository: RolRepositoryInterface):
        self.repository = repository

    def listar_roles(self) -> List[RolResponse]:
        return self.repository.get_all()

    def obtener_rol(self, id_rol: int) -> RolResponse:
        return self.repository.get_by_id(id_rol)

    def crear_rol(self, rol: RolCreate) -> RolResponse:
        return self.repository.create(rol)

    def actualizar_rol(self, id_rol: int, rol: RolUpdate) -> RolResponse:
        return self.repository.update(id_rol, rol)

    def eliminar_rol(self, id_rol: int) -> None:
        self.repository.delete(id_rol)
