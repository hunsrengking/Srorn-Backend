from pydantic import BaseModel
from typing import List, Optional


class AuthRequest(BaseModel):
    email: str
    password: str


class AuthPermission(BaseModel):
    id: int
    name: str


class AuthRole(BaseModel):
    id: int
    name: str


class AuthUser(BaseModel):
    id: int
    email: str
    username: str
    role_id: Optional[int] = None
    role: Optional[AuthRole] = None
    permissions: List[AuthPermission] = []


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUser
