from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.features.departments import service as department_service
from app.features.departments.models import DepartmentModel


class DepartmentController:
    @staticmethod
    def list_departments(db: Session):
        return department_service.getAllDepartment(db)

    @staticmethod
    def get_by_id(department_id: int, db: Session):
        department = department_service.getDepartmentById(db, department_id)
        if not department:
            raise HTTPException(
                status_code=404,
                detail=f"Department with id={department_id} not found",
            )
        return department

    @staticmethod
    def create(
        data: DepartmentModel,
        db: Session,
        current_user,
        background_tasks,
    ):
        return department_service.createDepartment(
            db,
            data.name,
            data.status_id,
            data.description,
            current_user=current_user,
            background_tasks=background_tasks,
        )

    @staticmethod
    def disable(department_id: int, db: Session):
        disabled_department = department_service.DisableDepartment(db, department_id)
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

        return department_service.addMemberToDepartment(db, department_id, user_id)

    @staticmethod
    def remove_member(department_id: int, user_id: int, db: Session):
        return department_service.removeMemberFromDepartment(db, department_id, user_id)
