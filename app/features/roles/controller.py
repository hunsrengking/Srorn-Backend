from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.features.roles.service import RoleService
from app.features.roles.models import RoleRequest


class RoleController:
    @staticmethod
    def list_roles(db: Session):
        roles = RoleService.getAllRole(db)
        return [
            {
                "id": role.id,
                "name": role.name,
                "description": getattr(role, "description", None),
                "permissions": [
                    permission.name
                    for permission in getattr(role, "permissions", [])
                ],
            }
            for role in roles
        ]

    @staticmethod
    def get_by_id(role_id: int, db: Session):
        role = RoleService.getRoleById(db, role_id)
        if not role:
            raise HTTPException(
                status_code=404,
                detail=f"Role with id={role_id} not found",
            )
        return {
            "id": role.id,
            "name": role.name,
            "description": getattr(role, "description", None),
            "permissions": [
                {"id": p.id, "name": p.name, "group": p.group}
                for p in getattr(role, "permissions", [])
            ],
        }

    @staticmethod
    def create(data: RoleRequest, db: Session):
        if not data.name:
            raise HTTPException(status_code=400, detail="Role name required")

        role = RoleService.createRole(db, data.name, data.description)
        return {
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "permissions": [],
        }

    @staticmethod
    def disable(role_id: int, db: Session):
        return RoleService.disableRole(db, role_id)

    @staticmethod
    def update_permissions(role_id: int, data: RoleRequest, db: Session):
        role = RoleService.updateRolePermissionsById(db, role_id, data.permissions)
        return {
            "id": role.id,
            "name": role.name,
            "permissions": [{"id": p.id, "name": p.name} for p in role.permissions],
        }

    @staticmethod
    def list_permissions(db: Session):
        permissions = RoleService.getAllPermissions(db)
        return [
            {
                "id": permission.id,
                "name": permission.name,
                "group": permission.group,
            }
            for permission in permissions
        ]
