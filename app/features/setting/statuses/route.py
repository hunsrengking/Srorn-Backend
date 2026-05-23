from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.setting.statuses.controller import StatusController

router = APIRouter(prefix="/api")


@router.get("/status")
def getAllStatus(db: Session = Depends(get_db)):
    return StatusController.get_all_status(db)


@router.get("/category")
def getAllCategory(db: Session = Depends(get_db)):
    return StatusController.get_all_category(db)


@router.get("/priority")
def getAllPriority(db: Session = Depends(get_db)):
    return StatusController.get_all_priority(db)
