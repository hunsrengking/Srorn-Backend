from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.auth.controller import AuthController
from app.features.auth.models import LoginRequest

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return AuthController.login(payload, db)


@router.post("/logout")
def logout(request: Request):
    return AuthController.logout(request)
