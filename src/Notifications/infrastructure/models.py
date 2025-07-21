"""
Database models for Notification (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.core.db import Base


class NotificationModel(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"),
                     nullable=False, index=True)
    device_id = Column(Integer, ForeignKey(
        "devices.id"), nullable=True, index=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("UserModel", back_populates="notifications")
    device = relationship("DeviceModel", back_populates="notifications")

    def __repr__(self):
        return f"<NotificationModel(id={self.id}, user_id={self.user_id}, is_read={self.is_read})>"
