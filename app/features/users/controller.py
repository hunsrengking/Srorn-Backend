from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.features.users.service import UserService
from app.features.users.models import UserRequest


class UserController:
    @staticmethod
    def getUsers(db: Session):
        return UserService.getAllUser(db)

    @staticmethod
    def getById(user_id: int, db: Session):
        user = UserService.getUserById(db, user_id)
        if not user:
            raise HTTPException(
                status_code=404, detail=f"User with id={user_id} not found"
            )
        return user

    @staticmethod
    def create(data: UserRequest, db: Session):
        missing_fields = [
            field
            for field in ("username", "email", "password", "role_id")
            if getattr(data, field) is None
        ]
        if missing_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field(s): {', '.join(missing_fields)}",
            )

        return (
            UserService.createUser(
                db,
                data.username,  # type: ignore[arg-type]
                data.email,  # type: ignore[arg-type]
                data.password,  # type: ignore[arg-type]
                data.role_id,  # type: ignore[arg-type]
                data.department_id,
                data.staff_id,
            ),
        )

    @staticmethod
    def update(user_id: int, data: UserRequest, db: Session):
        updated_user = UserService.updateUser(
            db,
            user_id,
            username=data.username,
            email=data.email,
            password=data.password,
            role_id=data.role_id,
            department_id=data.department_id,
            staff_id=data.staff_id,
        )
        if not updated_user:
            raise HTTPException(
                status_code=404, detail=f"User with id={user_id} not found"
            )
        return updated_user

    @staticmethod
    def delete(user_id: int, db: Session):
        deleted_user = UserService.deleteUser(db, user_id)
        if not deleted_user:
            raise HTTPException(
                status_code=404, detail=f"User with id={user_id} not found"
            )
        return {"message": f"User with id={user_id} has been deleted"}

    @staticmethod
    def admin_change_password(user_id: int, data: UserRequest, db: Session):
        password = data.password or data.new_password
        return UserService.admin_change_password(db, user_id, password)  # type: ignore

    @staticmethod
    def change_password(user_id: int, data: UserRequest, db: Session):
        return UserService.change_password(
            db,
            user_id,
            data.old_password,
            data.new_password,
        )

    @staticmethod
    def getUsersWithoutDepartment(db: Session):
        return UserService.getUsersWithoutDepartment(db)
