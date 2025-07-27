from sqlalchemy.orm import Session
from src.AutomationRules.domain.models import AutomationRule


class AutomationRuleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, rule: AutomationRule) -> AutomationRule:
        self.db.add(rule)
        self.db.commit()
        self.db.refresh(rule)
        return rule

    def get_by_id(self, rule_id: int) -> AutomationRule:
        return self.db.query(AutomationRule).filter(AutomationRule.id == rule_id).first()

    def get_by_user(self, user_id: int) -> list[AutomationRule]:
        return self.db.query(AutomationRule).filter(AutomationRule.user_id == user_id).all()

    def update(self, rule: AutomationRule) -> AutomationRule:
        self.db.commit()
        self.db.refresh(rule)
        return rule

    def delete(self, rule: AutomationRule) -> None:
        self.db.delete(rule)
        self.db.commit()

    def list_all(self) -> list[AutomationRule]:
        return self.db.query(AutomationRule).all()
