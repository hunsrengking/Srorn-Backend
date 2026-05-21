from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.controllers.office_controller import OfficeController
from app.models.office_model import OfficeCreate, OfficeResponse, OfficeUpdate
from app.middlewares.auth_middlewares import get_current_user

router = APIRouter(prefix="/api", tags=["Offices"])


@router.post("/offices", response_model=OfficeResponse)
def create_office(
    office: OfficeCreate, 
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return OfficeController.creates(office, db, current_user, background_tasks)


@router.get("/offices", response_model=list[OfficeResponse])
def findAll(db: Session = Depends(get_db)):
    return OfficeController.findAll(db)


@router.get("/offices/{office_id}", response_model=OfficeResponse)
def get_office(office_id: int, db: Session = Depends(get_db)):
    return OfficeController.findById(office_id, db)


@router.put("/offices/{office_id}", response_model=OfficeResponse)
def update_office(
    office_id: int, office: OfficeUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user), background_tasks: BackgroundTasks = BackgroundTasks()
):
    return OfficeController.updated(office_id, office, db, current_user, background_tasks)

@router.delete("/offices/{office_id}")
def delete_office(office_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user), background_tasks: BackgroundTasks = BackgroundTasks()):
    return OfficeController.deleted(office_id, db, current_user, background_tasks)