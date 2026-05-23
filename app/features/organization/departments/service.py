from fastapi import BackgroundTasks, HTTPException
from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.features.organization.departments.schema import Department
from app.features.notifications.service import NotificationService
from app.features.users.schema import User


class DepartmentService:
    @staticmethod
    def getAllDepartment(db):
        return db.query(Department).filter(Department.status_id == 1).all()

    @staticmethod
    def getDepartmentById(db, department_id: int):
        rows = (
            db.query(
                Department.id.label("department_id"),
                Department.name.label("department_name"),
                Department.status_id.label("status_id"),
                User.id.label("user_id"),
                User.username.label("username"),
                User.email.label("email"),
            )
            .outerjoin(User, User.department_id == Department.id)
            .filter(Department.id == department_id)
            .all()
        )

        if not rows:
            return None

        department = {
            "id": rows[0].department_id,
            "name": rows[0].department_name,
            "status_id": rows[0].status_id,
            "members": [],
        }

        for row in rows:
            if row.user_id:
                department["members"].append(
                    {
                        "id": row.user_id,
                        "username": row.username,
                        "email": row.email,
                    }
                )

        return department

    @staticmethod
    def createDepartment(
        db,
        name: str,
        status_id: int,
        description: str,
        current_user=None,
        background_tasks: BackgroundTasks | None = None,
    ):
        new_department = Department(
            name=name,
            status_id=status_id,
            description=description,
        )
        try:
            db.add(new_department)
            db.commit()
            db.refresh(new_department)

            if current_user and background_tasks:
                telegram_msg = (
                    f"<b>New Department Created:</b> {new_department.name}\n"
                    f"<b>Description:</b> {new_department.description or 'No description'}\n"
                    f"<b>Created by:</b> {current_user.username}\n"
                    "==============================\n"
                )
                NotificationService.notify_action(
                    db=db,
                    user=current_user,
                    title="New Department Created",
                    message=f"Department {new_department.name} has been added",
                    link="/departments",
                    notification_type="department",
                    background_tasks=background_tasks,
                    telegram_message=telegram_msg,
                )

            return new_department
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Department with this name already exists.",
            )

    @staticmethod
    def DisableDepartment(db: Session, department_id: int):
        department = (
            db.query(Department)
            .filter(Department.id == department_id, Department.status_id == 1)
            .first()
        )

        if not department:
            raise HTTPException(
                status_code=404,
                detail="Department not found or already disabled",
            )

        has_active_users = db.query(
            exists().where(User.department_id == department_id, User.is_delete == 0)
        ).scalar()

        if has_active_users:
            raise HTTPException(
                status_code=400,
                detail="Cannot disable department with active users",
            )

        department.status_id = 2  # type: ignore

        try:
            db.commit()
            db.refresh(department)
        except Exception as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(exc))

        return department

    @staticmethod
    def addMemberToDepartment(db: Session, department_id: int, user_id: int):
        department = (
            db.query(Department)
            .filter(Department.id == department_id, Department.status_id == 1)
            .first()
        )

        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

        user = db.query(User).filter(User.id == user_id, User.is_delete == 0).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.department_id == department_id:  # type: ignore
            raise HTTPException(status_code=400, detail="User already in this department")

        user.department_id = department_id  # type: ignore

        try:
            db.commit()
            db.refresh(user)
            return {"message": "Member added successfully"}
        except Exception as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(exc))

    @staticmethod
    def removeMemberFromDepartment(db: Session, department_id: int, user_id: int):
        user = (
            db.query(User)
            .filter(
                User.id == user_id,
                User.department_id == department_id,
                User.is_delete == 0,
            )
            .first()
        )

        if not user:
            raise HTTPException(status_code=404, detail="User not found in this department")

        user.department_id = None  # type: ignore

        try:
            db.commit()
            db.refresh(user)
            return {"message": "Member removed successfully"}
        except Exception as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(exc))
