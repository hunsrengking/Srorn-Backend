from sqlalchemy.orm import Session

from app.features.telegram import service as telegram_service
from app.features.telegram.models import TelegramConfigCreate, TelegramConfigUpdate


class TelegramController:
    @staticmethod
    def list_configs(db: Session):
        return telegram_service.list_configs(db)

    @staticmethod
    def create_config(data: TelegramConfigCreate, db: Session):
        return telegram_service.create_config(data, db)

    @staticmethod
    def update_config(config_id: int, data: TelegramConfigUpdate, db: Session):
        return telegram_service.update_config(config_id, data, db)

    @staticmethod
    def delete_config(config_id: int, db: Session):
        return telegram_service.delete_config(config_id, db)
