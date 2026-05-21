from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.features.auth import service as auth_service
from app.features.auth.models import LoginRequest


class AuthController:
    @staticmethod
    def login(payload: LoginRequest, db: Session):
        return auth_service.LoginService(
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
        auth_service.LogoutService(token)

        return {"message": "Logged out successfully"}
