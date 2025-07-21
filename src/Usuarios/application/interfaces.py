"""
Interfaces para el módulo de Users
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.Usuarios.domain.schemas import UserCreate, UserUpdate, UserResponse


class UserRepositoryInterface(ABC):
    """Interface para el repositorio de Users"""

    @abstractmethod
    def get_all(self) -> List[UserResponse]:
        """Obtener todos los usuarios"""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> UserResponse:
        """Obtener un usuario por ID"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserResponse]:
        """Obtener un usuario por email"""
        pass

    @abstractmethod
    def create(self, user: UserCreate) -> UserResponse:
        """Crear un nuevo usuario"""
        pass

    @abstractmethod
    def update(self, user_id: int, user: UserUpdate) -> UserResponse:
        """Actualizar un usuario existente"""
        pass

    @abstractmethod
    def update_password(self, user_id: int, new_password_hash: str) -> UserResponse:
        """Actualizar la contraseña de un usuario"""
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        """Eliminar un usuario"""
        pass

    @abstractmethod
    def verify_password(self, email: str, password: str) -> Optional[UserResponse]:
        """Verificar credenciales de usuario"""
        pass
