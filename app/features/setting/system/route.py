from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.setting.system.controller import SystemController
from app.features.setting.system.models import SystemSettingsResponse

router = APIRouter(prefix="/api/system-settings", tags=["System Settings"])


@router.get("", response_model=SystemSettingsResponse)
def get_system_settings(db: Session = Depends(get_db)):
    return SystemController.get_settings(db)


@router.post("", response_model=SystemSettingsResponse)
def update_system_settings(
    system_name: str = Form(...),
    auto_logout_enabled: bool = Form(False),
    auto_logout_time: int = Form(30),
    logo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    return SystemController.update_settings(
        db,
        system_name,
        logo,
        auto_logout_enabled,
        auto_logout_time,
    )
