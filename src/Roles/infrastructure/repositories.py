"""
Implementación del repositorio de Roles usando SQLAlchemy
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from src.Roles.application.interfaces import RoleRepositoryInterface
from src.Roles.domain.schemas import RoleCreate, RoleUpdate, RoleResponse
from src.Roles.infrastructure.models import RoleModel


class SqlAlchemyRoleRepository(RoleRepositoryInterface):
    """Implementación del repositorio usando SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[RoleResponse]:
        """Obtener todos los roles"""
        roles = self.db.query(RoleModel).all()
        return [RoleResponse.model_validate(role) for role in roles]

    def get_by_id(self, role_id: int) -> RoleResponse:
        """Obtener un rol por ID"""
        role = self.db.query(RoleModel).filter(RoleModel.id == role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rol con ID {role_id} no encontrado"
            )
        return RoleResponse.model_validate(role)

    def create(self, role: RoleCreate) -> RoleResponse:
        """Crear un nuevo rol"""
        try:
            db_role = RoleModel(**role.model_dump())
            self.db.add(db_role)
            self.db.commit()
            self.db.refresh(db_role)
            return RoleResponse.model_validate(db_role)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un rol con el nombre '{role.name}'"
            )

    def update(self, role_id: int, role: RoleUpdate) -> RoleResponse:
        """Actualizar un rol existente"""
        db_role = self.db.query(RoleModel).filter(
            RoleModel.id == role_id).first()
        if not db_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rol con ID {role_id} no encontrado"
            )

        # Actualizar solo los campos que no son None
        update_data = role.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_role, field, value)

        try:
            self.db.commit()
            self.db.refresh(db_role)
            return RoleResponse.model_validate(db_role)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un rol con el nombre especificado"
            )

    def delete(self, role_id: int) -> None:
        """Eliminar un rol"""
        db_role = self.db.query(RoleModel).filter(
            RoleModel.id == role_id).first()
        if not db_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rol con ID {role_id} no encontrado"
            )

        self.db.delete(db_role)
        self.db.commit()
