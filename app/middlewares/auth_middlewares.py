import inspect
from functools import wraps
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.features.auth.service import AuthService
from app.features.users.service import UserService
from app.features.roles.service import RoleService
import logging

auth_scheme = HTTPBearer(auto_error=False)
logger = logging.getLogger("app.auth")
PRIVILEGED_ROLE_NAMES = {"admin", "super admin", "superadmin"}


def _normalize_role_name(role_name: str | None) -> str:
    return (role_name or "").strip().lower().replace("_", " ").replace("-", " ")


def is_privileged_role(role) -> bool:
    role_name = _normalize_role_name(getattr(role, "name", None))
    compact_role_name = role_name.replace(" ", "")
    return (
        role_name in PRIVILEGED_ROLE_NAMES or compact_role_name in PRIVILEGED_ROLE_NAMES
    )


def user_has_permission(current_user, permission_name: str) -> bool:
    role = getattr(current_user, "role", None)
    if not role:
        return False

    if is_privileged_role(role):
        return True

    user_permissions = [p.name for p in getattr(role, "permissions", [])]
    return permission_name in user_permissions


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if credentials is None or not credentials.credentials:
        logger.debug("No Authorization header provided.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        payload = AuthService.decode_access_token(token)
    except Exception as e:
        # decode_access_token typically raises on invalid/expired token
        logger.warning("Token decode failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not payload:
        logger.warning("Token decode returned empty payload.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3) Ensure 'sub' present (or the claim name you use)
    user_id = payload.get("sub")
    if not user_id:
        logger.warning("Token payload missing 'sub': %s", payload)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: missing subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4) Retrieve user from DB
    try:
        user = UserService.getUserById(db, int(user_id))
    except Exception as e:
        logger.error("Error fetching user from DB (id=%s): %s", user_id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    if not user:
        logger.info("User not found for id=%s", user_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def requirepermissions(permission_name: str):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(
            *args, current_user=Depends(get_current_user), **kwargs
        ):
            role = getattr(current_user, "role", None)
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="No role assigned"
                )
            if not user_has_permission(current_user, permission_name):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
                )
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, current_user=Depends(get_current_user), **kwargs):
            role = getattr(current_user, "role", None)
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="No role assigned"
                )
            if not user_has_permission(current_user, permission_name):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
                )
            return func(*args, **kwargs)

        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

    return decorator


def require_permission(permission_name: str):
    async def check_permission(current_user=Depends(get_current_user)):
        role = getattr(current_user, "role", None)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="No role assigned"
            )
        if not user_has_permission(current_user, permission_name):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {permission_name} is required",
            )
        return current_user

    return check_permission
