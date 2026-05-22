from typing import Optional

from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    role_id: int | None = None
    department_id: Optional[int] = None
    is_locked: int = 0
    failed_attempts: int = 0
    staff_id: Optional[int] = None
    old_password: str | None = None
    new_password: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role_id: int
    department_id: Optional[int] = None
    staff_id: Optional[int] = None
    is_locked: int = 0
    failed_attempts: int = 0

    class Config:
        from_attributes = True
