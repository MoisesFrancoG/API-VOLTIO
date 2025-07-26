from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.AutomationRules.domain.schemas import AutomationRuleCreate, AutomationRuleUpdate, AutomationRuleResponse
from src.AutomationRules.infrastructure.repositories import AutomationRuleRepository
from src.core.db import get_database
from src.core.auth_middleware import get_current_user
from src.Usuarios.domain.schemas import UserResponse

router = APIRouter(prefix="/api/v1/automation-rules",
                   tags=["Automation Rules"])


def get_repo(db: Session = Depends(get_database)) -> AutomationRuleRepository:
    return AutomationRuleRepository(db)


@router.post("/", response_model=AutomationRuleResponse, status_code=201)
def create_rule(
    rule: AutomationRuleCreate,
    current_user: UserResponse = Depends(get_current_user),
    repo: AutomationRuleRepository = Depends(get_repo)
):
    return repo.create(rule, current_user.id)


@router.get("/", response_model=List[AutomationRuleResponse])
def list_rules(
    current_user: UserResponse = Depends(get_current_user),
    repo: AutomationRuleRepository = Depends(get_repo)
):
    return repo.list_by_user(current_user.id)


@router.get("/{rule_id}", response_model=AutomationRuleResponse)
def get_rule(
    rule_id: int,
    current_user: UserResponse = Depends(get_current_user),
    repo: AutomationRuleRepository = Depends(get_repo)
):
    rule = repo.get_by_id(rule_id, current_user.id)
    if not rule:
        raise HTTPException(status_code=404, detail="Regla no encontrada")
    return rule


@router.put("/{rule_id}", response_model=AutomationRuleResponse)
def update_rule(
    rule_id: int,
    rule: AutomationRuleUpdate,
    current_user: UserResponse = Depends(get_current_user),
    repo: AutomationRuleRepository = Depends(get_repo)
):
    updated = repo.update(rule_id, rule, current_user.id)
    if not updated:
        raise HTTPException(
            status_code=404, detail="Regla no encontrada o sin permiso")
    return updated


@router.delete("/{rule_id}", status_code=204)
def delete_rule(
    rule_id: int,
    current_user: UserResponse = Depends(get_current_user),
    repo: AutomationRuleRepository = Depends(get_repo)
):
    deleted = repo.delete(rule_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=404, detail="Regla no encontrada o sin permiso")
    return None
