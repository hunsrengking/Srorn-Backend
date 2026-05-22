from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.staff.controller import StaffController
from app.features.staff.models import StaffRequest, StaffResponse
from app.middlewares.auth_middlewares import get_current_user, require_permission

router = APIRouter(prefix="/api/staff", tags=["Staff"])


@router.get("", response_model=list[StaffResponse])
def get_all_staff(db: Session = Depends(get_db)):
    return StaffController.get_all(db)


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    return StaffController.get_by_id(staff_id, db)


@router.post("", response_model=StaffResponse)
def create_staff(
    data: StaffRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return StaffController.create(data, db, current_user, background_tasks)


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(
    staff_id: int,
    data: StaffRequest,
    db: Session = Depends(get_db),
):
    return StaffController.update(staff_id, data, db)


@router.delete("/{staff_id}")
def delete_staff(
    staff_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_permission("delete_staff")),
):
    return StaffController.delete(staff_id, db)
