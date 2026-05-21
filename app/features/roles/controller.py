from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.features.roles import service as role_service
from app.features.roles.models import RoleCreateReq, RolePermsReq


class RoleController:
    @staticmethod
    def list_roles(db: Session):
        roles = role_service.getAllRole(db)
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
        role = role_service.getRoleById(db, role_id)
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
    def create(data: RoleCreateReq, db: Session):
        role = role_service.createRole(db, data.name, data.description)
        return {
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "permissions": [],
        }

    @staticmethod
    def disable(role_id: int, db: Session):
        return role_service.disableRole(db, role_id)

    @staticmethod
    def update_permissions(role_id: int, data: RolePermsReq, db: Session):
        role = role_service.updateRolePermissionsById(db, role_id, data.permissions)
        return {
            "id": role.id,
            "name": role.name,
            "permissions": [{"id": p.id, "name": p.name} for p in role.permissions],
        }

    @staticmethod
    def list_permissions(db: Session):
        permissions = role_service.getAllPermissions(db)
        return [
            {
                "id": permission.id,
                "name": permission.name,
                "group": permission.group,
            }
            for permission in permissions
        ]
