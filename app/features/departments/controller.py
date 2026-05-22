from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.features.departments.service import DepartmentService
from app.features.departments.models import DepartmentRequest


class DepartmentController:
    @staticmethod
    def list_departments(db: Session):
        return DepartmentService.getAllDepartment(db)

    @staticmethod
    def get_by_id(department_id: int, db: Session):
        department = DepartmentService.getDepartmentById(db, department_id)
        if not department:
            raise HTTPException(
                status_code=404,
                detail=f"Department with id={department_id} not found",
            )
        return department

    @staticmethod
    def create(
        data: DepartmentRequest,
        db: Session,
        current_user,
        background_tasks,
    ):
        return DepartmentService.createDepartment(
            db,
            data.name,
            data.status_id,
            data.description,
            current_user=current_user,
            background_tasks=background_tasks,
        )

    @staticmethod
    def disable(department_id: int, db: Session):
        disabled_department = DepartmentService.DisableDepartment(db, department_id)
        if not disabled_department:
            raise HTTPException(
                status_code=404,
                detail=f"Department with id={department_id} not found",
            )
        return {"message": f"Department with id={department_id} has been disable"}

    @staticmethod
    def add_member(department_id: int, payload: dict, db: Session):
        user_id = payload.get("userId")
        if not user_id:
            raise HTTPException(status_code=400, detail="userId is required")

        return DepartmentService.addMemberToDepartment(db, department_id, user_id)

    @staticmethod
    def remove_member(department_id: int, user_id: int, db: Session):
        return DepartmentService.removeMemberFromDepartment(db, department_id, user_id)
