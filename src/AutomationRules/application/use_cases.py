from src.AutomationRules.repository.automation_rule_repository import AutomationRuleRepository
from src.AutomationRules.domain.models import AutomationRule
from src.AutomationRules.schemas.automation_rule_schema import (
    AutomationRuleCreate, AutomationRuleUpdate
)
from sqlalchemy.orm import Session
from datetime import time


def create_rule(db: Session, rule_in: AutomationRuleCreate, user_id: int) -> AutomationRule:
    rule = AutomationRule(**rule_in.dict(), user_id=user_id)
    repo = AutomationRuleRepository(db)
    return repo.create(rule)


def update_rule(db: Session, rule_id: int, rule_in: AutomationRuleUpdate) -> AutomationRule:
    repo = AutomationRuleRepository(db)
    rule = repo.get_by_id(rule_id)
    if not rule:
        return None
    for key, value in rule_in.dict(exclude_unset=True).items():
        setattr(rule, key, value)
    return repo.update(rule)


def delete_rule(db: Session, rule_id: int) -> bool:
    repo = AutomationRuleRepository(db)
    rule = repo.get_by_id(rule_id)
    if not rule:
        return False
    repo.delete(rule)
    return True


def get_rules_by_user(db: Session, user_id: int) -> list[AutomationRule]:
    repo = AutomationRuleRepository(db)
    return repo.get_by_user(user_id)


def set_rule_status(db: Session, rule_id: int, is_active: bool) -> AutomationRule:
    repo = AutomationRuleRepository(db)
    rule = repo.get_by_id(rule_id)
    if not rule:
        return None
    rule.is_active = is_active
    return repo.update(rule)


def set_rule_schedule(db: Session, rule_id: int, active_time_start: time, active_time_end: time) -> AutomationRule:
    repo = AutomationRuleRepository(db)
    rule = repo.get_by_id(rule_id)
    if not rule:
        return None
    rule.active_time_start = active_time_start
    rule.active_time_end = active_time_end
    return repo.update(rule)
