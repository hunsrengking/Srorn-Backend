from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.features.auth.service import AuthService
from app.features.auth.models import AuthRequest


class AuthController:
    @staticmethod
    def login(payload: AuthRequest, db: Session):
        return AuthService.LoginService(
            db=db,
            email=payload.email,
            password=payload.password,
        )

    @staticmethod
    def logout(request: Request):
        auth_header = request.headers.get("authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=400, detail="Missing Authorization")

        token = auth_header.split(" ", 1)[1]
        AuthService.LogoutService(token)

        return {"message": "Logged out successfully"}
