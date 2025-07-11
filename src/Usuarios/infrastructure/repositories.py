"""
Implementación del repositorio de Usuarios usando SQLAlchemy
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from passlib.context import CryptContext

from src.Usuarios.application.interfaces import UsuarioRepositoryInterface
from src.Usuarios.domain.schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from src.Usuarios.infrastructure.models import UsuarioModel

# Configuración para verificar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SqlAlchemyUsuarioRepository(UsuarioRepositoryInterface):
    """Implementación del repositorio usando SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[UsuarioResponse]:
        """Obtener todos los usuarios"""
        usuarios = self.db.query(UsuarioModel).all()
        return [UsuarioResponse.model_validate(usuario) for usuario in usuarios]

    def get_by_id(self, id_usuario: int) -> UsuarioResponse:
        """Obtener un usuario por ID"""
        usuario = self.db.query(UsuarioModel).filter(
            UsuarioModel.id_usuario == id_usuario
        ).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {id_usuario} no encontrado"
            )
        return UsuarioResponse.model_validate(usuario)

    def get_by_email(self, correo: str) -> Optional[UsuarioResponse]:
        """Obtener un usuario por email"""
        usuario = self.db.query(UsuarioModel).filter(
            UsuarioModel.correo == correo
        ).first()
        if usuario:
            return UsuarioResponse.model_validate(usuario)
        return None

    def create(self, usuario: UsuarioCreate) -> UsuarioResponse:
        """Crear un nuevo usuario"""
        try:
            db_usuario = UsuarioModel(**usuario.model_dump())
            self.db.add(db_usuario)
            self.db.commit()
            self.db.refresh(db_usuario)
            return UsuarioResponse.model_validate(db_usuario)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario con el email '{usuario.correo}'"
            )

    def update(self, id_usuario: int, usuario: UsuarioUpdate) -> UsuarioResponse:
        """Actualizar un usuario existente"""
        db_usuario = self.db.query(UsuarioModel).filter(
            UsuarioModel.id_usuario == id_usuario
        ).first()
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {id_usuario} no encontrado"
            )

        # Actualizar solo los campos que no son None
        update_data = usuario.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_usuario, field, value)

        try:
            self.db.commit()
            self.db.refresh(db_usuario)
            return UsuarioResponse.model_validate(db_usuario)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con el email especificado"
            )

    def update_password(self, id_usuario: int, nueva_contrasena_hash: str) -> UsuarioResponse:
        """Actualizar la contraseña de un usuario"""
        db_usuario = self.db.query(UsuarioModel).filter(
            UsuarioModel.id_usuario == id_usuario
        ).first()
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {id_usuario} no encontrado"
            )

        db_usuario.contrasena = nueva_contrasena_hash
        self.db.commit()
        self.db.refresh(db_usuario)
        return UsuarioResponse.model_validate(db_usuario)

    def delete(self, id_usuario: int) -> None:
        """Eliminar un usuario"""
        db_usuario = self.db.query(UsuarioModel).filter(
            UsuarioModel.id_usuario == id_usuario
        ).first()
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {id_usuario} no encontrado"
            )

        self.db.delete(db_usuario)
        self.db.commit()

    def verify_password(self, correo: str, contrasena: str) -> Optional[UsuarioResponse]:
        """Verificar credenciales de usuario"""
        usuario = self.db.query(UsuarioModel).filter(
            UsuarioModel.correo == correo
        ).first()

        if usuario and pwd_context.verify(contrasena, usuario.contrasena):
            return UsuarioResponse.model_validate(usuario)
        return None
