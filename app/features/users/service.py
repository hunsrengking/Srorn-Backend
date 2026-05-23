from typing import Optional

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import case
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.features.organization.departments.schema import Department
from app.features.setting.roles.schema import Role
from app.features.organization.staff.schema import Staff
from app.features.tickets.schema import Ticket
from app.features.users.schema import User

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


class UserService:
    @staticmethod
    def createUser(
        db,
        username: str,
        email: str,
        password: str,
        role_id: int,
        department_id: Optional[int] = None,
        staff_id: Optional[int] = None,
    ):
        try:
            if db.query(User).filter(User.email == email, User.is_delete == 0).first():
                raise HTTPException(status_code=400, detail="Email already exists.")

            if (
                db.query(User)
                .filter(User.username == username, User.is_delete == 0)
                .first()
            ):
                raise HTTPException(status_code=400, detail="Username already exists.")

            if (
                staff_id is not None
                and db.query(User)
                .filter(User.staff_id == staff_id, User.is_delete == 0)
                .first()
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Staff is already assigned to a user.",
                )

            hashed_password = pwd_context.hash(password)
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                role_id=role_id,
                department_id=department_id if department_id is not None else None,
                staff_id=staff_id if staff_id is not None else None,
                is_delete=0,
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(exc))

    @staticmethod
    def updateUser(
        db,
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        role_id: Optional[int] = None,
        department_id: Optional[int] = None,
        staff_id: Optional[int] = None,
    ):
        user = db.query(User).filter(User.id == user_id, User.is_delete == 0).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        if email and email != user.email:
            exists = (
                db.query(User)
                .filter(User.email == email, User.is_delete == 0, User.id != user_id)
                .first()
            )
            if exists:
                raise HTTPException(status_code=400, detail="Email already exists.")

        if username and username != user.username:
            exists = (
                db.query(User)
                .filter(
                    User.username == username,
                    User.is_delete == 0,
                    User.id != user_id,
                )
                .first()
            )
            if exists:
                raise HTTPException(status_code=400, detail="Username already exists.")

        if staff_id is not None and staff_id != user.staff_id:
            exists = (
                db.query(User)
                .filter(
                    User.staff_id == staff_id,
                    User.is_delete == 0,
                    User.id != user_id,
                )
                .first()
            )
            if exists:
                raise HTTPException(
                    status_code=400,
                    detail="Staff is already assigned to another user.",
                )

        if username is not None:
            user.username = username

        if email is not None:
            user.email = email

        if password:
            user.password = pwd_context.hash(password)

        if role_id is not None:
            user.role_id = role_id

        if department_id is not None:
            user.department_id = department_id

        if staff_id is not None:
            user.staff_id = staff_id

        try:
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Database integrity error.")
        except Exception as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(exc))

    @staticmethod
    def deleteUser(db, user_id: int):
        user = db.query(User).filter(User.id == user_id, User.is_delete == 0).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        ticket_exists = (
            db.query(Ticket).filter(Ticket.assigned_to_id == user_id).first()
        )

        if ticket_exists:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete user. User is assigned to one or more tickets.",
            )

        user.is_delete = 1
        try:
            db.commit()
            db.refresh(user)
        except Exception as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(exc))
        return user

    @staticmethod
    def admin_change_password(db, user_id: int, new_password: str):
        if not new_password or new_password.strip() == "":
            raise HTTPException(status_code=400, detail="Password cannot be empty.")

        user = db.query(User).filter(User.id == user_id, User.is_delete == 0).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"User with id={user_id} not found",
            )

        try:
            user.password = pwd_context.hash(new_password)
            db.commit()
            db.refresh(user)
            return {"message": "Password changed successfully"}
        except Exception as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(exc))

    @staticmethod
    def change_password(db, user_id: int, old_password, new_password: str):
        if not new_password or new_password.strip() == "":
            raise HTTPException(status_code=400, detail="New password cannot be empty.")

        if not old_password or old_password.strip() == "":
            raise HTTPException(status_code=400, detail="Old password cannot be empty.")

        user = db.query(User).filter(User.id == user_id, User.is_delete == 0).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"User with id={user_id} not found",
            )

        if not pwd_context.verify(old_password, user.password):
            raise HTTPException(status_code=400, detail="Old password is incorrect.")

        user.password = pwd_context.hash(new_password)
        try:
            db.commit()
            db.refresh(user)
        except Exception as exc:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(exc))
        return user

    @staticmethod
    def getUserByEmail(db, email: str):
        return db.query(User).filter(User.email == email, User.is_delete == 0).first()

    @staticmethod
    def getUserById(db, id: int):
        return (
            db.query(User)
            .options(
                joinedload(User.role).joinedload(Role.permissions),
                joinedload(User.staff),
            )
            .filter(User.id == id, User.is_delete == 0)
            .first()
        )

    @staticmethod
    def getAllUser(db):
        status_case = case(
            (User.is_locked == 1, "Locked"),
            (User.is_delete == 0, "Active"),
            else_="Deleted",
        )

        rows = (
            db.query(
                User.id,
                User.username,
                User.email,
                User.role_id,
                User.department_id,
                User.staff_id,
                User.is_delete,
                status_case.label("status"),
                Role.name.label("role_name"),
                Department.name.label("department_name"),
                Staff.display_name.label("staff_name"),
            )
            .join(Role, User.role_id == Role.id, isouter=True)
            .join(Department, User.department_id == Department.id, isouter=True)
            .join(Staff, User.staff_id == Staff.id, isouter=True)
            .filter(User.is_delete == 0)
            .all()
        )

        return [dict(row._mapping) for row in rows]

    @staticmethod
    def has_permission(user, permission_name: str):
        if not user.role:
            return False
        return any(
            permission.name == permission_name for permission in user.role.permissions
        )

    @staticmethod
    def getUsersWithoutDepartment(db):
        users = (
            db.query(
                User.id,
                User.username,
                User.email,
                Staff.display_name.label("display_name"),
            )
            .outerjoin(Staff, User.staff_id == Staff.id)
            .filter(User.is_delete == 0, User.department_id.is_(None))
            .all()
        )

        return [dict(row._mapping) for row in users]
