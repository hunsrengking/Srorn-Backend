from enum import Enum
from typing import Optional

from fastapi import APIRouter, Depends, BackgroundTasks, Query
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.organization.print.controller import PrintCardController
from app.features.organization.print.models import PrintCardRequest, PrintCardResponse
from app.middlewares.auth_middlewares import get_current_user

router = APIRouter(prefix="/api/organization", tags=["Organization"])


class EntityType(str, Enum):
    student = "student"
    staff = "staff"


# ── Templates ────────────────────────────────────────────────────────────────

@router.get("/templates/{entity_type}/{entity_id}/printcards")
def getPrintCardTemplateByEntity(
    entity_type: EntityType,
    entity_id: int,
    db: Session = Depends(get_db),
):
    if entity_type == EntityType.student:
        return PrintCardController.getPrintCardStudentTemplate(entity_id, db)
    elif entity_type == EntityType.staff:
        return PrintCardController.getPrintCardStaffTemplate(entity_id, db)


@router.get("/printcards")
def getPrintCardData(db: Session = Depends(get_db)):
    return PrintCardController.getPrintCardData(db)


@router.get("/printcards/stats")
def getPrintCardStats(db: Session = Depends(get_db)):
    return PrintCardController.getPrintCardStats(db)


@router.get("/printcards/{print_card_id}")
def getPrintCardById(
    print_card_id: int,
    db: Session = Depends(get_db),
):
    return PrintCardController.getPrintCardById(print_card_id, db)

@router.get("/printcards/entity/{entity_id}")
def getPrintCardByEntityId(
    entity_id: int,
    db: Session = Depends(get_db),
):
    return PrintCardController.getPrintCardByEntityId(entity_id, db)


@router.post("/printcards", response_model=PrintCardResponse)
def createPrintCard(
    print_card: PrintCardRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return PrintCardController.PrintCardNew(
        print_card, db, current_user, background_tasks
    )


@router.put("/printcards/{print_card_id}", response_model=PrintCardResponse)
def updatePrintCard(
    print_card_id: int,
    print_card: PrintCardRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return PrintCardController.UpdatePrintCard(
        print_card_id, print_card, db, current_user, background_tasks
    )
