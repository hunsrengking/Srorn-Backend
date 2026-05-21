from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.features.organization.controller import OrganizationController
from app.features.organization.models import PrintCardResponse, PrintCardCreate, PrintCardTemplate, PrintCardUpdate
from app.middlewares.auth_middlewares import get_current_user

router = APIRouter(prefix="/api/organization", tags=["Organization"])

@router.get("/templates/printcards", response_model=PrintCardTemplate)
def get_print_card_template(db: Session = Depends(get_db)):
    return OrganizationController.getAllPrintCardTemplate(db)

@router.get("/printcards", response_model=list[PrintCardResponse])
def get_print_card(db: Session = Depends(get_db)):
    return OrganizationController.getAllPrintCard(db)

@router.get("/printcards/{print_card_id}", response_model=PrintCardResponse)
def get_print_card_by_id(print_card_id: int, db: Session = Depends(get_db)):
    return OrganizationController.getAllPrintCardById(print_card_id, db)

@router.post("/printcards", response_model=PrintCardResponse)
def create_print_card(
    print_card: PrintCardCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    return OrganizationController.PrintCardNew(print_card, db, current_user, background_tasks)

@router.put("/printcards/{print_card_id}", response_model=PrintCardResponse)
def update_print_card(
    print_card_id: int,
    print_card: PrintCardUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    return OrganizationController.UpdatePrintCard(print_card_id, print_card, db, current_user, background_tasks)
