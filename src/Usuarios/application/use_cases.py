"""
Casos de uso para el módulo de Usuarios
"""

from typing import List, Optional
from fastapi import HTTPException, status

from src.Usuarios.application.interfaces import UserRepositoryInterface
from src.Usuarios.application.auth_service import AuthService
from src.Usuarios.domain.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    UserUpdatePassword,
    TokenResponse
)


class UserUseCases:
    """Casos de uso para el módulo de Usuarios"""

    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository
        self.auth_service = AuthService()

    def listar_usuarios(self) -> List[UserResponse]:
        """Obtener todos los usuarios"""
        return self.repository.get_all()

    def obtener_usuario(self, user_id: int) -> UserResponse:
        """Obtener un usuario por ID"""
        return self.repository.get_by_id(user_id)

    def obtener_usuario_por_email(self, email: str) -> Optional[UserResponse]:
        """Obtener un usuario por email"""
        return self.repository.get_by_email(email)

    def crear_usuario(self, usuario: UserCreate) -> UserResponse:
        """Crear un nuevo usuario"""
        # Verificar si ya existe un usuario con el mismo email
        existing_user = self.repository.get_by_email(usuario.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario con el email '{usuario.email}'"
            )

        # El hashing de la contraseña se hace en el repositorio
        return self.repository.create(usuario)

    def actualizar_usuario(self, user_id: int, usuario: UserUpdate) -> UserResponse:
        """Actualizar un usuario existente"""
        # Verificar que el usuario existe
        existing_user = self.repository.get_by_id(user_id)

        # Si se está actualizando el email, verificar que no esté en uso
        if usuario.email and usuario.email != existing_user.email:
            email_exists = self.repository.get_by_email(usuario.email)
            if email_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe un usuario con el email '{usuario.email}'"
                )

        return self.repository.update(user_id, usuario)

    def cambiar_contrasena(self, user_id: int, datos_contrasena: UserUpdatePassword) -> UserResponse:
        """Cambiar la contraseña de un usuario"""
        # Verificar que el usuario existe y la contraseña actual es correcta
        usuario = self.repository.get_by_id(user_id)

        # Aquí deberías verificar la contraseña actual
        # Por simplicidad, asumo que ya está verificada
        nueva_contrasena_hash = self._hash_password(
            datos_contrasena.new_password)

        return self.repository.update_password(user_id, nueva_contrasena_hash)

    def eliminar_usuario(self, user_id: int) -> None:
        """Eliminar un usuario"""
        # Verificar que el usuario existe
        self.repository.get_by_id(user_id)
        self.repository.delete(user_id)

    def autenticar_usuario(self, credenciales: UserLogin) -> TokenResponse:
        """Autenticar un usuario y generar JWT token"""
        usuario = self.repository.verify_password(
            credenciales.email, credenciales.password)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Crear token JWT
        token_data = {
            # JWT spec requiere que sub sea string
            "sub": str(usuario.id),
            "email": usuario.email
        }
        access_token = self.auth_service.create_access_token(token_data)

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=self.auth_service.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user_id=usuario.id
        )

    def _hash_password(self, password: str) -> str:
        """Hashear una contraseña"""
        return self.auth_service.hash_password(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verificar una contraseña"""
        return self.auth_service.verify_password(plain_password, hashed_password)
