import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.features.setting.telegram.models import TelegramConfigRequest
from app.features.setting.telegram.schema import TelegramConfig


class TelegramService:
    @staticmethod
    def getActiveTelegramConfig(db: Session):
        return db.query(TelegramConfig).filter(TelegramConfig.is_active == True).first()

    @staticmethod
    def SendTelegramMessageAsync(bot_token: str, chat_id: str, message: str):
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
        }
        requests.post(url, json=payload, timeout=10)

    @staticmethod
    def list_configs(db: Session):
        return db.query(TelegramConfig).all()

    @staticmethod
    def create_config(data: TelegramConfigRequest, db: Session):
        payload = data.model_dump(exclude_none=True)
        if not payload.get("bot_token") or not payload.get("chat_id"):
            raise HTTPException(status_code=400, detail="bot_token and chat_id are required")

        payload.setdefault("is_active", True)
        if payload["is_active"]:
            db.query(TelegramConfig).update({"is_active": False})

        config = TelegramConfig(**payload)
        db.add(config)
        db.commit()
        db.refresh(config)
        return config

    @staticmethod
    def update_config(
        config_id: int,
        data: TelegramConfigRequest,
        db: Session,
    ):
        config = db.query(TelegramConfig).filter_by(id=config_id).first()
        if not config:
            raise HTTPException(status_code=404, detail="Config not found")

        if data.is_active is True:
            db.query(TelegramConfig).update({"is_active": False})

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(config, key, value)

        db.commit()
        db.refresh(config)
        return config

    @staticmethod
    def delete_config(config_id: int, db: Session):
        config = db.query(TelegramConfig).filter_by(id=config_id).first()
        if not config:
            raise HTTPException(status_code=404, detail="Config not found")

        db.delete(config)
        db.commit()
        return {"message": "Deleted successfully"}
