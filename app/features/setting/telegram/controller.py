from sqlalchemy.orm import Session

from app.features.setting.telegram.service import TelegramService
from app.features.setting.telegram.models import TelegramConfigRequest


class TelegramController:
    @staticmethod
    def list_configs(db: Session):
        return TelegramService.list_configs(db)

    @staticmethod
    def create_config(data: TelegramConfigRequest, db: Session):
        return TelegramService.create_config(data, db)

    @staticmethod
    def update_config(config_id: int, data: TelegramConfigRequest, db: Session):
        return TelegramService.update_config(config_id, data, db)

    @staticmethod
    def delete_config(config_id: int, db: Session):
        return TelegramService.delete_config(config_id, db)
