from sqlalchemy import Column, Integer, String, Boolean, Float, Time, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AutomationRule(Base):
    __tablename__ = "automation_rules"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    trigger_device_mac = Column(String(17), nullable=False)
    trigger_metric = Column(String(32), nullable=False)
    comparison_operator = Column(String(16), nullable=False)
    threshold_value = Column(Float, nullable=True)
    action_device_mac = Column(String(17), nullable=False)
    action_capability_id = Column(Integer, nullable=False)
    action_payload = Column(Text, nullable=False)
    active_time_start = Column(Time, nullable=True)
    active_time_end = Column(Time, nullable=True)
    user_id = Column(Integer,nullable=False)
