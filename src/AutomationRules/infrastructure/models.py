from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Time
from sqlalchemy.orm import relationship
from src.core.db import Base

class AutomationRuleModel(Base):
    __tablename__ = "automation_rules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    trigger_device_id = Column(Integer, nullable=False)
    action_device_id = Column(Integer, nullable=False)
    trigger_metric = Column(String(50), nullable=False)
    comparison_operator = Column(String(50), nullable=False)
    threshold_value = Column(Float, nullable=False)
    action_capability_id = Column(Integer, nullable=False)
    action_payload = Column(String(50), nullable=False)
    active_time_start = Column(String(8), nullable=False)  # HH:MM:SS
    active_time_end = Column(String(8), nullable=False)    # HH:MM:SS
    is_active = Column(Boolean, default=True, nullable=False)

    user = relationship("UserModel", back_populates="automation_rules")

    def __repr__(self):
        return f"<AutomationRuleModel(id={self.id}, user_id={self.user_id}, name='{self.name}')>"
