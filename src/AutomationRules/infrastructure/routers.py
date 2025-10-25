from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.Usuarios.domain.schemas import UserResponse
from src.core.db import get_database
from src.AutomationRules.schemas.automation_rule_schema import (
    AutomationRuleCreate, AutomationRuleUpdate, AutomationRuleOut
)
from src.AutomationRules.application.use_cases import (
    create_rule, update_rule, delete_rule, get_rules_by_user, set_rule_status, set_rule_schedule
)
from typing import List
from datetime import time
from src.core.auth_middleware import get_current_user

router = APIRouter(prefix="/api/automation-rules", tags=["Automation Rules"])

# 1. Crear una regla de automatización


@router.post("/", response_model=AutomationRuleOut, status_code=status.HTTP_201_CREATED)
def create_automation_rule(rule_in: AutomationRuleCreate, db: Session = Depends(get_database), current_user: UserResponse = Depends(get_current_user)):
    rule_data = rule_in.dict()
    rule = create_rule(db, AutomationRuleCreate(
        **rule_data), user_id=current_user.id)
    return rule

# 2. Editar una regla existente


@router.put("/{rule_id}", response_model=AutomationRuleOut)
def update_automation_rule(rule_id: int, rule_in: AutomationRuleUpdate, db: Session = Depends(get_database)):
    rule = update_rule(db, rule_id, rule_in)
    if not rule:
        raise HTTPException(status_code=404, detail="Regla no encontrada")
    return rule

# 3. Eliminar una regla


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_automation_rule(rule_id: int, db: Session = Depends(get_database)):
    success = delete_rule(db, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Regla no encontrada")
    return

# 4. Listar reglas de un usuario autenticado


@router.get("/me", response_model=List[AutomationRuleOut])
def list_my_automation_rules(db: Session = Depends(get_database), current_user: UserResponse = Depends(get_current_user)):
    rules = get_rules_by_user(db, current_user.id)
    return rules

# 5. Activar/desactivar una regla


@router.patch("/{rule_id}/status", response_model=AutomationRuleOut)
def set_automation_rule_status(rule_id: int, is_active: bool, db: Session = Depends(get_database)):
    rule = set_rule_status(db, rule_id, is_active)
    if not rule:
        raise HTTPException(status_code=404, detail="Regla no encontrada")
    return rule

# 6. Configurar horarios personalizados


@router.patch("/{rule_id}/schedule", response_model=AutomationRuleOut)
def set_automation_rule_schedule(rule_id: int, active_time_start: time, active_time_end: time, db: Session = Depends(get_database)):
    rule = set_rule_schedule(db, rule_id, active_time_start, active_time_end)
    if not rule:
        raise HTTPException(status_code=404, detail="Regla no encontrada")
    return rule
