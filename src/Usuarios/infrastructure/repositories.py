"""
Implementación del repositorio de Users usando SQLAlchemy
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from passlib.context import CryptContext

from src.Usuarios.application.interfaces import UserRepositoryInterface
from src.Usuarios.domain.schemas import UserCreate, UserUpdate, UserResponse
from src.Usuarios.infrastructure.models import UserModel

# Configuración para verificar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SqlAlchemyUserRepository(UserRepositoryInterface):
    """Implementación del repositorio usando SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[UserResponse]:
        """Obtener todos los usuarios"""
        users = self.db.query(UserModel).all()
        return [UserResponse.model_validate(user) for user in users]

    def get_by_id(self, user_id: int) -> UserResponse:
        """Obtener un usuario por ID"""
        user = self.db.query(UserModel).filter(
            UserModel.id == user_id
        ).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        return UserResponse.model_validate(user)

    def get_by_email(self, email: str) -> Optional[UserResponse]:
        """Obtener un usuario por email"""
        user = self.db.query(UserModel).filter(
            UserModel.email == email
        ).first()
        if user:
            return UserResponse.model_validate(user)
        return None

    def create(self, user: UserCreate) -> UserResponse:
        """Crear un nuevo usuario"""
        try:
            # Usar los valores del esquema UserCreate (que ya tiene role_id=2 por defecto)
            user_data = user.model_dump()

            # Hashear la contraseña
            user_data['password_hash'] = pwd_context.hash(
                user_data.pop('password'))

            db_user = UserModel(**user_data)
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return UserResponse.model_validate(db_user)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario con el email '{user.email}'"
            )

    def update(self, user_id: int, user: UserUpdate) -> UserResponse:
        """Actualizar un usuario existente"""
        db_user = self.db.query(UserModel).filter(
            UserModel.id == user_id
        ).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )

        # Actualizar solo los campos que no son None
        update_data = user.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_user, field, value)

        try:
            self.db.commit()
            self.db.refresh(db_user)
            return UserResponse.model_validate(db_user)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con el email especificado"
            )

    def update_password(self, user_id: int, new_password_hash: str) -> UserResponse:
        """Actualizar la contraseña de un usuario"""
        db_user = self.db.query(UserModel).filter(
            UserModel.id == user_id
        ).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )

        db_user.password_hash = new_password_hash
        self.db.commit()
        self.db.refresh(db_user)
        return UserResponse.model_validate(db_user)

    def delete(self, user_id: int) -> None:
        """Eliminar un usuario"""
        db_user = self.db.query(UserModel).filter(
            UserModel.id == user_id
        ).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )

        self.db.delete(db_user)
        self.db.commit()

    def verify_password(self, email: str, password: str) -> Optional[UserResponse]:
        """Verificar credenciales de usuario"""
        user = self.db.query(UserModel).filter(
            UserModel.email == email
        ).first()

        if user and pwd_context.verify(password, user.password_hash):
            return UserResponse.model_validate(user)
        return None
