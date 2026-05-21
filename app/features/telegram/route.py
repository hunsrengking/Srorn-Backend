from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.telegram.controller import TelegramController
from app.features.telegram.models import (
    TelegramConfigCreate,
    TelegramConfigResponse,
    TelegramConfigUpdate,
)
from app.middlewares.auth_middlewares import require_permission

router = APIRouter(prefix="/api/telegram", tags=["Telegram"])


@router.get("", response_model=list[TelegramConfigResponse])
def list_configs(db: Session = Depends(get_db)):
    return TelegramController.list_configs(db)


@router.post("", response_model=TelegramConfigResponse)
def create_config(
    data: TelegramConfigCreate,
    db: Session = Depends(get_db),
):
    return TelegramController.create_config(data, db)


@router.put("/{config_id}", response_model=TelegramConfigResponse)
def update_config(
    config_id: int,
    data: TelegramConfigUpdate,
    db: Session = Depends(get_db),
):
    return TelegramController.update_config(config_id, data, db)


@router.delete("/{config_id}")
def delete_config(
    config_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_permission("delete_telegram")),
):
    return TelegramController.delete_config(config_id, db)
