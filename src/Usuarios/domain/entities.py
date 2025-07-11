"""
Entidades de dominio para Usuario
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    """Entidad de dominio para Usuario"""
    id_usuario: Optional[int]
    nombre_usuario: str
    correo: str
    contrasena: str
    id_rol: int

    def __post_init__(self):
        """Validaciones de dominio"""
        if not self.nombre_usuario or len(self.nombre_usuario.strip()) == 0:
            raise ValueError("El nombre de usuario no puede estar vacío")

        if not self.correo or "@" not in self.correo:
            raise ValueError("El correo debe tener un formato válido")

        if not self.contrasena or len(self.contrasena) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")

        if self.id_rol <= 0:
            raise ValueError("El ID de rol debe ser un número positivo")

    def cambiar_contrasena(self, nueva_contrasena: str) -> None:
        """Cambiar la contraseña del usuario"""
        if len(nueva_contrasena) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        self.contrasena = nueva_contrasena

    def es_valido_para_login(self) -> bool:
        """Verificar si el usuario es válido para login"""
        return (
            self.nombre_usuario and
            self.correo and
            self.contrasena and
            self.id_rol > 0
        )
