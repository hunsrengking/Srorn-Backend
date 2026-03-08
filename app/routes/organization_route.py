from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.controllers.organization_controller import OrganizationController
from app.models.organization_model import PrintCardResponse, PrintCardCreate

router = APIRouter(prefix="/api/organization", tags=["Organization"])


@router.get("/printcards", response_model=list[PrintCardResponse])
def get_print_card(db: Session = Depends(get_db)):
    return OrganizationController.getAllPrintCard(db)

@router.get("/printcards/{print_card_id}", response_model=PrintCardResponse)
def get_print_card_by_id(print_card_id: int, db: Session = Depends(get_db)):
    return OrganizationController.getAllPrintCardById(print_card_id, db)

@router.post("/printcards", response_model=PrintCardResponse)
def create_print_card(print_card: PrintCardCreate, db: Session = Depends(get_db)):
    return OrganizationController.PrintCardNew(print_card, db)