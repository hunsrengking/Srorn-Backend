from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.users.controller import UserController
from app.features.users.models import UserRequest
from app.middlewares.auth_middlewares import require_permission

router = APIRouter(prefix="/api/users")


@router.get("")
def list_users(
    db: Session = Depends(get_db),
    user=Depends(require_permission("VIEW_USER")),
):
    return UserController.getUsers(db)


@router.get("/without/department")
def get_users_without_department(db: Session = Depends(get_db)):
    return UserController.getUsersWithoutDepartment(db)


@router.get("/{id}")
def get_user_by_id(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(require_permission("VIEW_USER")),
):
    return UserController.getById(id, db)


@router.post("")
def create_user(
    data: UserRequest,
    db: Session = Depends(get_db),
    user=Depends(require_permission("CREATE_USER")),
):
    return UserController.create(data, db)


@router.put("/{user_id}")
def update_user(
    user_id: int,
    data: UserRequest,
    db: Session = Depends(get_db),
    user=Depends(require_permission("UPDATE_USER")),
):
    return UserController.update(user_id, data, db)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_permission("DELETE_USER")),
):
    return UserController.delete(user_id, db)


@router.patch("/{user_id}/change-password")
def admin_change_user_password(
    user_id: int,
    data: UserRequest,
    db: Session = Depends(get_db),
    user=Depends(require_permission("CHANGE_USER_PASSWORD")),
):
    return UserController.admin_change_password(user_id, data, db)


@router.post("/{user_id}/changepassword")
def change_user_password(
    user_id: int,
    data: UserRequest,
    db: Session = Depends(get_db),
    user=Depends(require_permission("CHANGE_OWN_PASSWORD")),
):
    return UserController.change_password(user_id, data, db)
