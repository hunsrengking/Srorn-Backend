from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.features.users import service as user_service
from app.features.users.models import ChangePasswordModel, UserModel


class UserController:
    @staticmethod
    def list_users(db: Session):
        return user_service.getAllUser(db)

    @staticmethod
    def get_by_id(user_id: int, db: Session):
        user = user_service.getUserById(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with id={user_id} not found")
        return user

    @staticmethod
    def create(data: UserModel, db: Session):
        return (
            user_service.create_user(
                db,
                data.username,
                data.email,
                data.password,
                data.role_id,
                data.department_id,
                data.staff_id,
            ),
        )

    @staticmethod
    def update(user_id: int, data: UserModel, db: Session):
        updated_user = user_service.update_user(
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
            raise HTTPException(status_code=404, detail=f"User with id={user_id} not found")
        return updated_user

    @staticmethod
    def delete(user_id: int, db: Session):
        deleted_user = user_service.delete_user(db, user_id)
        if not deleted_user:
            raise HTTPException(status_code=404, detail=f"User with id={user_id} not found")
        return {"message": f"User with id={user_id} has been deleted"}

    @staticmethod
    def admin_change_password(user_id: int, data: dict, db: Session):
        password = data.get("password")
        return user_service.admin_change_password(db, user_id, password)  # type: ignore

    @staticmethod
    def change_password(user_id: int, data: ChangePasswordModel, db: Session):
        return user_service.change_password(
            db,
            user_id,
            data.old_password,
            data.new_password,
        )

    @staticmethod
    def get_users_without_department(db: Session):
        return user_service.getUsersWithoutDepartment(db)
