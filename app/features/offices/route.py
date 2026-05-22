from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.offices.controller import OfficeController
from app.features.offices.models import OfficeRequest, OfficeResponse
from app.middlewares.auth_middlewares import get_current_user

router = APIRouter(prefix="/api/offices", tags=["Offices"])


@router.post("", response_model=OfficeResponse)
def create_office(
    office: OfficeRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return OfficeController.creates(office, db, current_user, background_tasks)


@router.get("", response_model=list[OfficeResponse])
def findAll(db: Session = Depends(get_db)):
    return OfficeController.findAll(db)


@router.get("/{office_id}", response_model=OfficeResponse)
def get_office(office_id: int, db: Session = Depends(get_db)):
    return OfficeController.findById(office_id, db)


@router.put("/{office_id}", response_model=OfficeResponse)
def update_office(
    office_id: int,
    office: OfficeRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return OfficeController.updated(office_id, office, db, current_user, background_tasks)


@router.delete("/{office_id}")
def delete_office(
    office_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return OfficeController.deleted(office_id, db, current_user, background_tasks)
