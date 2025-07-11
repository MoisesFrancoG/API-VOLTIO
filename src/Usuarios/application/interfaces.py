"""
Interfaces para el módulo de Usuarios
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.Usuarios.domain.schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse


class UsuarioRepositoryInterface(ABC):
    """Interface para el repositorio de Usuarios"""

    @abstractmethod
    def get_all(self) -> List[UsuarioResponse]:
        """Obtener todos los usuarios"""
        pass

    @abstractmethod
    def get_by_id(self, id_usuario: int) -> UsuarioResponse:
        """Obtener un usuario por ID"""
        pass

    @abstractmethod
    def get_by_email(self, correo: str) -> Optional[UsuarioResponse]:
        """Obtener un usuario por email"""
        pass

    @abstractmethod
    def create(self, usuario: UsuarioCreate) -> UsuarioResponse:
        """Crear un nuevo usuario"""
        pass

    @abstractmethod
    def update(self, id_usuario: int, usuario: UsuarioUpdate) -> UsuarioResponse:
        """Actualizar un usuario existente"""
        pass

    @abstractmethod
    def update_password(self, id_usuario: int, nueva_contrasena_hash: str) -> UsuarioResponse:
        """Actualizar la contraseña de un usuario"""
        pass

    @abstractmethod
    def delete(self, id_usuario: int) -> None:
        """Eliminar un usuario"""
        pass

    @abstractmethod
    def verify_password(self, correo: str, contrasena: str) -> Optional[UsuarioResponse]:
        """Verificar credenciales de usuario"""
        pass
