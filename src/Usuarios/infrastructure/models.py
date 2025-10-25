"""
Modelos de base de datos para User (SQLAlchemy)
"""


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.core.db import Base
from src.Roles.infrastructure.models import RoleModel


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    # Relación con la tabla roles
    role = relationship("RoleModel", back_populates="users")
 
    notifications = relationship("NotificationModel", back_populates="user")

    def __repr__(self):
        return f"<UserModel(id={self.id}, username='{self.username}', email='{self.email}')>"
