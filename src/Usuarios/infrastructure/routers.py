"""
Rutas FastAPI para el módulo de Usuarios
"""

from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.core.db import get_database
from src.core.auth_middleware import get_current_user, require_admin, require_any_authenticated
from src.Usuarios.domain.schemas import (
    UserCreate,
    UserRegister,
    UserUpdate,
    UserResponse,
    UserLogin,
    UserUpdatePassword,
    TokenResponse
)
from src.Usuarios.application.use_cases import UserUseCases
from src.Usuarios.infrastructure.database import get_user_use_cases


router = APIRouter(prefix="/users", tags=["Users"])


def get_use_cases(db: Session = Depends(get_database)) -> UserUseCases:
    """Dependency para obtener los casos de uso de Usuario"""
    return get_user_use_cases(db)


# Endpoint público para login
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Autenticar usuario",
    description="Autentica un usuario con email y contraseña, retorna JWT token"
)
def login_usuario(credenciales: UserLogin, use_cases: UserUseCases = Depends(get_use_cases)):
    """Autenticar un usuario y obtener token JWT"""
    return use_cases.autenticar_usuario(credenciales)


# Endpoint protegido - información del usuario actual
@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener información del usuario actual",
    description="Obtiene la información del usuario autenticado mediante JWT"
)
def obtener_usuario_actual(current_user: UserResponse = Depends(get_current_user)):
    """Obtener información del usuario autenticado"""
    return current_user


# Endpoints que requieren autenticación (cualquier usuario)
@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Listar todos los usuarios",
    description="Obtiene una lista de todos los usuarios (requiere autenticación)"
)
def listar_usuarios(
    current_user: UserResponse = Depends(get_current_user),
    use_cases: UserUseCases = Depends(get_use_cases)
):
    """Obtener todos los usuarios (requiere autenticación)"""
    return use_cases.listar_usuarios()


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Obtiene un usuario específico por su ID (requiere autenticación)"
)
def obtener_usuario(
    user_id: int,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: UserUseCases = Depends(get_use_cases)
):
    """Obtener un usuario por ID (requiere autenticación)"""
    return use_cases.obtener_usuario(user_id)


@router.get(
    "/email/{email}",
    response_model=UserResponse,
    summary="Obtener usuario por email",
    description="Obtiene un usuario específico por su email (requiere autenticación)"
)
def obtener_usuario_por_email(
    email: str,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: UserUseCases = Depends(get_use_cases)
):
    """Obtener un usuario por email (requiere autenticación)"""
    usuario = use_cases.obtener_usuario_por_email(email)
    if not usuario:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con email '{email}' no encontrado"
        )
    return usuario


# Endpoint público para registro de usuario
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea un nuevo usuario regular en el sistema (endpoint público). Todos los usuarios registrados tienen rol 'User' por defecto."
)
def registrar_usuario(usuario_data: UserRegister, use_cases: UserUseCases = Depends(get_use_cases)):
    """
    Registrar un nuevo usuario (público)
    
    - **username**: Nombre de usuario único
    - **email**: Email válido del usuario  
    - **password**: Contraseña (mínimo 6 caracteres)
    
    Todos los usuarios registrados públicamente reciben automáticamente el rol 'User' (ID=2).
    Solo los administradores pueden crear usuarios con otros roles usando el endpoint /users/.
    """
    # Crear UserCreate con role_id fijo en 2 (User regular)
    usuario_create = UserCreate(
        username=usuario_data.username,
        email=usuario_data.email,
        password=usuario_data.password,
        role_id=2  # Siempre rol de usuario regular
    )
    
    return use_cases.crear_usuario(usuario_create)


# Endpoints que requieren permisos de administrador
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo usuario (Admin)",
    description="Crea un nuevo usuario en el sistema (requiere permisos de admin)"
)
def crear_usuario(
    usuario: UserCreate,
    current_user: UserResponse = Depends(require_admin()),
    use_cases: UserUseCases = Depends(get_use_cases)
):
    """Crear un nuevo usuario (requiere admin)"""
    return use_cases.crear_usuario(usuario)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario",
    description="Actualiza la información de un usuario (requiere ser el propietario o admin)"
)
def actualizar_usuario(
    user_id: int,
    usuario: UserUpdate,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: UserUseCases = Depends(get_use_cases)
):
    """Actualizar un usuario existente (requiere ser propietario o admin)"""
    from src.core.auth_middleware import user_can_modify_resource
    if not user_can_modify_resource(current_user, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes actualizar tu propio perfil o ser administrador"
        )
    return use_cases.actualizar_usuario(user_id, usuario)


@router.patch(
    "/{user_id}/password",
    response_model=UserResponse,
    summary="Cambiar contraseña",
    description="Cambia la contraseña de un usuario (requiere ser el propietario o admin)"
)
def cambiar_contrasena(
    user_id: int,
    datos_contrasena: UserUpdatePassword,
    current_user: UserResponse = Depends(get_current_user),
    use_cases: UserUseCases = Depends(get_use_cases)
):
    """Cambiar la contraseña de un usuario (requiere ser propietario o admin)"""
    from src.core.auth_middleware import user_can_modify_resource
    if not user_can_modify_resource(current_user, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes cambiar tu propia contraseña o ser administrador"
        )
    return use_cases.cambiar_contrasena(user_id, datos_contrasena)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario (Admin)",
    description="Elimina un usuario del sistema (requiere permisos de admin)"
)
def eliminar_usuario(
    user_id: int,
    current_user: UserResponse = Depends(require_admin()),
    use_cases: UserUseCases = Depends(get_use_cases)
):
    """Eliminar un usuario (requiere admin)"""
    use_cases.eliminar_usuario(user_id)
