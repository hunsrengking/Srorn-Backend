from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.auth.controller import AuthController
from app.features.auth.models import AuthRequest, AuthResponse

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/login", response_model=AuthResponse)
def login(data: AuthRequest, db: Session = Depends(get_db)):
    return AuthController.login(data, db)


@router.post("/logout")
def logout(request: Request):
    return AuthController.logout(request)
