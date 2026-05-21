from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.services.system_service import SystemService
from app.models.system_model import SystemSettingsResponse
from typing import Optional

router = APIRouter(prefix="/api/system-settings", tags=["System Settings"])

@router.get("", response_model=SystemSettingsResponse)
def get_system_settings(db: Session = Depends(get_db)):
    return SystemService.get_settings(db)

@router.post("", response_model=SystemSettingsResponse)
def update_system_settings(
    system_name: str = Form(...),
    auto_logout_enabled: bool = Form(False),
    auto_logout_time: int = Form(30),
    logo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    return SystemService.update_settings(db, system_name, logo, auto_logout_enabled, auto_logout_time)
