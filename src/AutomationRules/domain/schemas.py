from pydantic import BaseModel, Field
from typing import Optional

class AutomationRuleBase(BaseModel):
    name: str = Field(..., max_length=100)
    trigger_device_id: int
    action_device_id: int
    trigger_metric: str
    comparison_operator: str
    threshold_value: float
    action_capability_id: int
    action_payload: str
    active_time_start: str  # Format: HH:MM:SS
    active_time_end: str    # Format: HH:MM:SS
    is_active: bool = True

class AutomationRuleCreate(AutomationRuleBase):
    pass

class AutomationRuleUpdate(AutomationRuleBase):
    pass

class AutomationRuleResponse(AutomationRuleBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
