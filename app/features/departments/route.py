from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.departments.controller import DepartmentController
from app.features.departments.models import DepartmentModel
from app.middlewares.auth_middlewares import require_permission

router = APIRouter(prefix="/api/department")


@router.get("")
def list_department(
    db: Session = Depends(get_db),
    user=Depends(require_permission("VIEW_DEPARTMENT")),
):
    return DepartmentController.list_departments(db)


@router.get("/{id}")
def getDepartmentById(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(require_permission("VIEW_DEPARTMENT")),
):
    return DepartmentController.get_by_id(id, db)


@router.post("")
def createDepartment(
    data: DepartmentModel,
    db: Session = Depends(get_db),
    user=Depends(require_permission("CREATE_DEPARTMENT")),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    return DepartmentController.create(data, db, user, background_tasks)


@router.delete("/{id}")
def DisableDepartment(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(require_permission("DELETE_DEPARTMENT")),
):
    return DepartmentController.disable(id, db)


@router.post("/{id}/members/add")
def add_department_member(id: int, payload: dict, db: Session = Depends(get_db)):
    return DepartmentController.add_member(id, payload, db)


@router.delete("/{id}/members/{user_id}remove")
def remove_department_member(
    id: int,
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_permission("remove_department_member")),
):
    return DepartmentController.remove_member(id, user_id, db)
