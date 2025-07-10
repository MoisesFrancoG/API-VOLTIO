"""
Implementación del repositorio de Roles usando SQLAlchemy
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from src.Roles.application.interfaces import RolRepositoryInterface
from src.Roles.domain.schemas import RolCreate, RolUpdate, RolResponse
from src.Roles.infrastructure.models import RolModel


class SqlAlchemyRolRepository(RolRepositoryInterface):
    """Implementación del repositorio usando SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[RolResponse]:
        """Obtener todos los roles"""
        roles = self.db.query(RolModel).all()
        return [RolResponse.model_validate(rol) for rol in roles]

    def get_by_id(self, id_rol: int) -> RolResponse:
        """Obtener un rol por ID"""
        rol = self.db.query(RolModel).filter(RolModel.id_rol == id_rol).first()
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rol con ID {id_rol} no encontrado"
            )
        return RolResponse.model_validate(rol)

    def create(self, rol: RolCreate) -> RolResponse:
        """Crear un nuevo rol"""
        try:
            db_rol = RolModel(**rol.model_dump())
            self.db.add(db_rol)
            self.db.commit()
            self.db.refresh(db_rol)
            return RolResponse.model_validate(db_rol)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un rol con el nombre '{rol.nombre}'"
            )

    def update(self, id_rol: int, rol: RolUpdate) -> RolResponse:
        """Actualizar un rol existente"""
        db_rol = self.db.query(RolModel).filter(
            RolModel.id_rol == id_rol).first()
        if not db_rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rol con ID {id_rol} no encontrado"
            )

        # Actualizar solo los campos que no son None
        update_data = rol.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_rol, field, value)

        try:
            self.db.commit()
            self.db.refresh(db_rol)
            return RolResponse.model_validate(db_rol)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un rol con el nombre especificado"
            )

    def delete(self, id_rol: int) -> None:
        """Eliminar un rol"""
        db_rol = self.db.query(RolModel).filter(
            RolModel.id_rol == id_rol).first()
        if not db_rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rol con ID {id_rol} no encontrado"
            )

        self.db.delete(db_rol)
        self.db.commit()
