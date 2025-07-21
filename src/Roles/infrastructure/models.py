"""
Modelos de base de datos para Role (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.db import Base


class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(String(255), nullable=True)

    # Relación con la tabla users
    users = relationship("UserModel", back_populates="role")

    def __repr__(self):
        return f"<RoleModel(id={self.id}, name='{self.name}')>"
