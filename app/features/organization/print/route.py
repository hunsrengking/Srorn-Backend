from enum import Enum
from typing import Optional

from fastapi import APIRouter, Depends, BackgroundTasks, Query
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.organization.print.controller import OrganizationController
from app.features.organization.print.models import PrintCardRequest, PrintCardResponse
from app.middlewares.auth_middlewares import get_current_user

router = APIRouter(prefix="/api/organization", tags=["Organization"])


class EntityType(str, Enum):
    student = "student"
    staff   = "staff"


# ── Templates ────────────────────────────────────────────────────────────────

@router.get("/templates/printcards")
def get_print_card_template(db: Session = Depends(get_db)):
    return OrganizationController.getAllPrintCardTemplate(db)


@router.get("/templates/{entity_type}/{entity_id}/printcards")
def get_print_card_template_by_entity(
    entity_type: EntityType,
    entity_id: int,
    db: Session = Depends(get_db),
):
    if entity_type == EntityType.student:
        return OrganizationController.getPrintCardStudentTemplate(entity_id, db)
    elif entity_type == EntityType.staff:
        return OrganizationController.getPrintCardStaffTemplate(entity_id, db)


# ── Print Cards ───────────────────────────────────────────────────────────────

@router.get("/printcards")
def get_print_cards(
    entry_id: Optional[int] = Query(default=None),
    entity_type: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    return OrganizationController.getAllPrintCard(db, entry_id=entry_id, entity_type=entity_type)



@router.get("/printcards/{print_card_id}")
def get_print_card_by_id(
    print_card_id: int,
    db: Session = Depends(get_db),
):
    return OrganizationController.getAllPrintCardById(print_card_id, db)


@router.post("/printcards", response_model=PrintCardResponse)
def create_print_card(
    print_card: PrintCardRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return OrganizationController.PrintCardNew(
        print_card, db, current_user, background_tasks
    )


@router.put("/printcards/{print_card_id}", response_model=PrintCardResponse)
def update_print_card(
    print_card_id: int,
    print_card: PrintCardRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return OrganizationController.UpdatePrintCard(
        print_card_id, print_card, db, current_user, background_tasks
    )
