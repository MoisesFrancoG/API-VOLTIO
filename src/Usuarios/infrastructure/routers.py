"""
Rutas FastAPI para el módulo de Usuarios
"""

from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.core.db import get_database
from src.core.auth_middleware import get_current_user, require_admin, require_any_authenticated
from src.Usuarios.domain.schemas import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioLogin,
    UsuarioUpdatePassword,
    TokenResponse
)
from src.Usuarios.application.use_cases import UsuarioUseCases
from src.Usuarios.infrastructure.database import get_usuario_use_cases


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def get_use_cases(db: Session = Depends(get_database)) -> UsuarioUseCases:
    """Dependency para obtener los casos de uso de Usuario"""
    return get_usuario_use_cases(db)


# Endpoint público para login
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Autenticar usuario",
    description="Autentica un usuario con email y contraseña, retorna JWT token"
)
def login_usuario(credenciales: UsuarioLogin, use_cases: UsuarioUseCases = Depends(get_use_cases)):
    """Autenticar un usuario y obtener token JWT"""
    return use_cases.autenticar_usuario(credenciales)


# Endpoint protegido - información del usuario actual
@router.get(
    "/me",
    response_model=UsuarioResponse,
    summary="Obtener información del usuario actual",
    description="Obtiene la información del usuario autenticado mediante JWT"
)
def obtener_usuario_actual(current_user: UsuarioResponse = Depends(get_current_user)):
    """Obtener información del usuario autenticado"""
    return current_user


# Endpoints que requieren autenticación (cualquier usuario)
@router.get(
    "/",
    response_model=List[UsuarioResponse],
    summary="Listar todos los usuarios",
    description="Obtiene una lista de todos los usuarios (requiere autenticación)"
)
def listar_usuarios(
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: UsuarioUseCases = Depends(get_use_cases)
):
    """Obtener todos los usuarios (requiere autenticación)"""
    return use_cases.listar_usuarios()


@router.get(
    "/{id_usuario}",
    response_model=UsuarioResponse,
    summary="Obtener usuario por ID",
    description="Obtiene un usuario específico por su ID (requiere autenticación)"
)
def obtener_usuario(
    id_usuario: int,
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: UsuarioUseCases = Depends(get_use_cases)
):
    """Obtener un usuario por ID (requiere autenticación)"""
    return use_cases.obtener_usuario(id_usuario)


@router.get(
    "/email/{correo}",
    response_model=UsuarioResponse,
    summary="Obtener usuario por email",
    description="Obtiene un usuario específico por su email (requiere autenticación)"
)
def obtener_usuario_por_email(
    correo: str,
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: UsuarioUseCases = Depends(get_use_cases)
):
    """Obtener un usuario por email (requiere autenticación)"""
    usuario = use_cases.obtener_usuario_por_email(correo)
    if not usuario:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con email '{correo}' no encontrado"
        )
    return usuario


# Endpoint público para registro de usuario
@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea un nuevo usuario en el sistema (endpoint público)"
)
def registrar_usuario(usuario: UsuarioCreate, use_cases: UsuarioUseCases = Depends(get_use_cases)):
    """Registrar un nuevo usuario (público)"""
    return use_cases.crear_usuario(usuario)


# Endpoints que requieren permisos de administrador
@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo usuario (Admin)",
    description="Crea un nuevo usuario en el sistema (requiere permisos de admin)"
)
def crear_usuario(
    usuario: UsuarioCreate,
    current_user: UsuarioResponse = Depends(require_admin()),
    use_cases: UsuarioUseCases = Depends(get_use_cases)
):
    """Crear un nuevo usuario (requiere admin)"""
    return use_cases.crear_usuario(usuario)


@router.put(
    "/{id_usuario}",
    response_model=UsuarioResponse,
    summary="Actualizar usuario",
    description="Actualiza la información de un usuario (requiere ser el propietario o admin)"
)
def actualizar_usuario(
    id_usuario: int,
    usuario: UsuarioUpdate,
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: UsuarioUseCases = Depends(get_use_cases)
):
    """Actualizar un usuario existente (requiere ser propietario o admin)"""
    from src.core.auth_middleware import user_can_modify_resource
    if not user_can_modify_resource(current_user, id_usuario):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes actualizar tu propio perfil o ser administrador"
        )
    return use_cases.actualizar_usuario(id_usuario, usuario)


@router.patch(
    "/{id_usuario}/password",
    response_model=UsuarioResponse,
    summary="Cambiar contraseña",
    description="Cambia la contraseña de un usuario (requiere ser el propietario o admin)"
)
def cambiar_contrasena(
    id_usuario: int,
    datos_contrasena: UsuarioUpdatePassword,
    current_user: UsuarioResponse = Depends(get_current_user),
    use_cases: UsuarioUseCases = Depends(get_use_cases)
):
    """Cambiar la contraseña de un usuario (requiere ser propietario o admin)"""
    from src.core.auth_middleware import user_can_modify_resource
    if not user_can_modify_resource(current_user, id_usuario):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes cambiar tu propia contraseña o ser administrador"
        )
    return use_cases.cambiar_contrasena(id_usuario, datos_contrasena)


@router.delete(
    "/{id_usuario}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario (Admin)",
    description="Elimina un usuario del sistema (requiere permisos de admin)"
)
def eliminar_usuario(
    id_usuario: int,
    current_user: UsuarioResponse = Depends(require_admin()),
    use_cases: UsuarioUseCases = Depends(get_use_cases)
):
    """Eliminar un usuario (requiere admin)"""
    use_cases.eliminar_usuario(id_usuario)
