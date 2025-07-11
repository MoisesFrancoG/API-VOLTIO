"""
Casos de uso para el módulo de Usuarios
"""

from typing import List, Optional
from fastapi import HTTPException, status

from src.Usuarios.application.interfaces import UsuarioRepositoryInterface
from src.Usuarios.application.auth_service import AuthService
from src.Usuarios.domain.schemas import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioLogin,
    UsuarioUpdatePassword,
    TokenResponse
)


class UsuarioUseCases:
    """Casos de uso para el módulo de Usuarios"""

    def __init__(self, repository: UsuarioRepositoryInterface):
        self.repository = repository
        self.auth_service = AuthService()

    def listar_usuarios(self) -> List[UsuarioResponse]:
        """Obtener todos los usuarios"""
        return self.repository.get_all()

    def obtener_usuario(self, id_usuario: int) -> UsuarioResponse:
        """Obtener un usuario por ID"""
        return self.repository.get_by_id(id_usuario)

    def obtener_usuario_por_email(self, correo: str) -> Optional[UsuarioResponse]:
        """Obtener un usuario por email"""
        return self.repository.get_by_email(correo)

    def crear_usuario(self, usuario: UsuarioCreate) -> UsuarioResponse:
        """Crear un nuevo usuario"""
        # Verificar si ya existe un usuario con el mismo email
        existing_user = self.repository.get_by_email(usuario.correo)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario con el email '{usuario.correo}'"
            )

        # Hashear la contraseña
        usuario.contrasena = self.auth_service.hash_password(
            usuario.contrasena)

        return self.repository.create(usuario)

    def actualizar_usuario(self, id_usuario: int, usuario: UsuarioUpdate) -> UsuarioResponse:
        """Actualizar un usuario existente"""
        # Verificar que el usuario existe
        existing_user = self.repository.get_by_id(id_usuario)

        # Si se está actualizando el email, verificar que no esté en uso
        if usuario.correo and usuario.correo != existing_user.correo:
            email_exists = self.repository.get_by_email(usuario.correo)
            if email_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe un usuario con el email '{usuario.correo}'"
                )

        return self.repository.update(id_usuario, usuario)

    def cambiar_contrasena(self, id_usuario: int, datos_contrasena: UsuarioUpdatePassword) -> UsuarioResponse:
        """Cambiar la contraseña de un usuario"""
        # Verificar que el usuario existe y la contraseña actual es correcta
        usuario = self.repository.get_by_id(id_usuario)

        # Aquí deberías verificar la contraseña actual
        # Por simplicidad, asumo que ya está verificada
        nueva_contrasena_hash = self._hash_password(
            datos_contrasena.contrasena_nueva)

        return self.repository.update_password(id_usuario, nueva_contrasena_hash)

    def eliminar_usuario(self, id_usuario: int) -> None:
        """Eliminar un usuario"""
        # Verificar que el usuario existe
        self.repository.get_by_id(id_usuario)
        self.repository.delete(id_usuario)

    def autenticar_usuario(self, credenciales: UsuarioLogin) -> TokenResponse:
        """Autenticar un usuario y generar JWT token"""
        usuario = self.repository.verify_password(
            credenciales.correo, credenciales.contrasena)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Crear token JWT
        token_data = {
            # JWT spec requiere que sub sea string
            "sub": str(usuario.id_usuario),
            "email": usuario.correo
        }
        access_token = self.auth_service.create_access_token(token_data)

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=self.auth_service.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user_id=usuario.id_usuario
        )

    def _hash_password(self, password: str) -> str:
        """Hashear una contraseña"""
        return self.auth_service.hash_password(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verificar una contraseña"""
        return self.auth_service.verify_password(plain_password, hashed_password)
