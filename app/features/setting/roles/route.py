from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.setting.roles.controller import RoleController
from app.features.setting.roles.models import RoleRequest
from app.middlewares.auth_middlewares import require_permission

router = APIRouter(prefix="/api")


@router.get("/role")
def listRoles(db: Session = Depends(get_db)):
    return RoleController.list_roles(db)


@router.get("/role/{role_id}")
def getRole(role_id: int, db: Session = Depends(get_db)):
    return RoleController.get_by_id(role_id, db)


@router.post("/role")
def createRole(data: RoleRequest, db: Session = Depends(get_db)):
    return RoleController.create(data, db)


@router.delete("/role/{role_id}")
def DisableRole(
    role_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_permission("delete_role")),
):
    return RoleController.disable(role_id, db)


@router.put("/role/{role_id}/permissions")
def updatePermissions(
    role_id: int,
    data: RoleRequest,
    db: Session = Depends(get_db),
):
    return RoleController.update_permissions(role_id, data, db)


@router.get("/permissions")
def listPermissions(db: Session = Depends(get_db)):
    return RoleController.list_permissions(db)
