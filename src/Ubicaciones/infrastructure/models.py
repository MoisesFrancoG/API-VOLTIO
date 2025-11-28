"""
Modelos de base de datos para Location (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from src.core.db import Base


class LocationModel(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<LocationModel(id={self.id}, name='{self.name}')>"
