"""
Database models for AutomationRule (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Time, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.core.db import Base


class AutomationRuleModel(Base):
    __tablename__ = "automation_rules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)

    # Trigger configuration
    trigger_device_id = Column(Integer, ForeignKey(
        "devices.id", ondelete="CASCADE"), nullable=False, index=True)
    trigger_metric = Column(String(50), nullable=False, index=True)
    comparison_operator = Column(String(30), nullable=False)
    threshold_value = Column(Float, nullable=False)

    # Action configuration
    action_device_id = Column(Integer, ForeignKey(
        "devices.id", ondelete="CASCADE"), nullable=False, index=True)
    action_capability_id = Column(Integer, ForeignKey(
        "device_capabilities.id"), nullable=False, index=True)
    action_payload = Column(Text, nullable=False)

    # Time restrictions (optional)
    active_time_start = Column(Time, nullable=True)
    active_time_end = Column(Time, nullable=True)

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("UserModel")
    trigger_device = relationship(
        "DeviceModel", foreign_keys=[trigger_device_id])
    action_device = relationship(
        "DeviceModel", foreign_keys=[action_device_id])
    action_capability = relationship("DeviceCapabilityModel")

    def __repr__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"<AutomationRuleModel(id={self.id}, name='{self.name}', user_id={self.user_id}, status={status})>"
