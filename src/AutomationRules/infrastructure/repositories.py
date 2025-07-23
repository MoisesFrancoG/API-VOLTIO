from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.AutomationRules.infrastructure.models import AutomationRuleModel
from src.AutomationRules.domain.schemas import AutomationRuleCreate, AutomationRuleUpdate, AutomationRuleResponse
from src.Sensores.infrastructure.models import DeviceModel

class AutomationRuleRepository:
    def __init__(self, db: Session):
        self.db = db

    def _check_device_ownership(self, device_id: int, user_id: int):
        device = self.db.query(DeviceModel).filter(DeviceModel.id == device_id, DeviceModel.user_id == user_id).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El usuario no es propietario del dispositivo.")

    def create(self, rule: AutomationRuleCreate, user_id: int) -> AutomationRuleResponse:
        self._check_device_ownership(rule.trigger_device_id, user_id)
        self._check_device_ownership(rule.action_device_id, user_id)
        db_rule = AutomationRuleModel(**rule.model_dump(), user_id=user_id)
        self.db.add(db_rule)
        self.db.commit()
        self.db.refresh(db_rule)
        return AutomationRuleResponse.model_validate(db_rule)

    def list_by_user(self, user_id: int) -> List[AutomationRuleResponse]:
        rules = self.db.query(AutomationRuleModel).filter(AutomationRuleModel.user_id == user_id).all()
        return [AutomationRuleResponse.model_validate(r) for r in rules]

    def get_by_id(self, rule_id: int, user_id: int) -> Optional[AutomationRuleResponse]:
        rule = self.db.query(AutomationRuleModel).filter(AutomationRuleModel.id == rule_id, AutomationRuleModel.user_id == user_id).first()
        if not rule:
            return None
        return AutomationRuleResponse.model_validate(rule)

    def update(self, rule_id: int, rule: AutomationRuleUpdate, user_id: int) -> Optional[AutomationRuleResponse]:
        db_rule = self.db.query(AutomationRuleModel).filter(AutomationRuleModel.id == rule_id, AutomationRuleModel.user_id == user_id).first()
        if not db_rule:
            return None
        self._check_device_ownership(rule.trigger_device_id, user_id)
        self._check_device_ownership(rule.action_device_id, user_id)
        for field, value in rule.model_dump().items():
            setattr(db_rule, field, value)
        self.db.commit()
        self.db.refresh(db_rule)
        return AutomationRuleResponse.model_validate(db_rule)

    def delete(self, rule_id: int, user_id: int) -> bool:
        db_rule = self.db.query(AutomationRuleModel).filter(AutomationRuleModel.id == rule_id, AutomationRuleModel.user_id == user_id).first()
        if not db_rule:
            return False
        self.db.delete(db_rule)
        self.db.commit()
        return True
