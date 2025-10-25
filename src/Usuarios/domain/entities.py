"""
Entidades de dominio para User
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Entidad de dominio para User"""
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    role_id: int

    def __post_init__(self):
        """Validaciones de dominio"""
        if not self.username or len(self.username.strip()) == 0:
            raise ValueError("El nombre de usuario no puede estar vacío")

        if not self.email or "@" not in self.email:
            raise ValueError("El email debe tener un formato válido")

        if not self.password_hash or len(self.password_hash) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")

        if self.role_id <= 0:
            raise ValueError("El ID de rol debe ser un número positivo")

    def change_password(self, new_password_hash: str) -> None:
        """Cambiar la contraseña del usuario"""
        if len(new_password_hash) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        self.password_hash = new_password_hash

    def is_valid_for_login(self) -> bool:
        """Verificar si el usuario es válido para login"""
        return (
            self.username and
            self.email and
            self.password_hash and
            self.role_id > 0
        )
