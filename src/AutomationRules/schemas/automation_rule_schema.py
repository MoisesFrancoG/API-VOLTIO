from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import time


class AutomationRuleBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = True
    trigger_device_mac: str = Field(..., min_length=17, max_length=17)
    trigger_metric: str
    comparison_operator: str
    threshold_value: Optional[float]
    action_device_mac: str = Field(..., min_length=17, max_length=17)
    action_capability_id: int
    action_payload: str
    active_time_start: Optional[time]
    active_time_end: Optional[time]

    @validator('trigger_metric')
    def validate_trigger_metric(cls, v):
        allowed = ["motion", "temperature", "humidity", "lux", "voltage", "current",
                   "power", "energy", "frequency", "pf", "workday_start", "workday_end"]
        if v not in allowed:
            raise ValueError(f"trigger_metric debe ser uno de: {allowed}")
        return v

    @validator('comparison_operator')
    def validate_comparison_operator(cls, v):
        allowed = ["GREATER_THAN", "LESS_THAN", "EQUAL", "NOT_EQUAL"]
        if v not in allowed:
            raise ValueError(f"comparison_operator debe ser uno de: {allowed}")
        return v

    @validator('action_capability_id')
    def validate_action_capability_id(cls, v):
        allowed = [1, 2]
        if v not in allowed:
            raise ValueError(
                "action_capability_id debe ser 1 (RELAY_CONTROL) o 2 (INFRARED_EMITTER)")
        return v

# Para crear, no se pide user_id ni id


class AutomationRuleCreate(AutomationRuleBase):
    pass

# Para actualizar, tampoco se pide user_id ni id


class AutomationRuleUpdate(AutomationRuleBase):
    pass

# Para salida, incluye id y user_id


class AutomationRuleOut(AutomationRuleBase):
    id: int
    user_id: int
