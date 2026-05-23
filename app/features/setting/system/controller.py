from sqlalchemy.orm import Session

from app.features.setting.system.service import SystemService


class SystemController:
    @staticmethod
    def get_settings(db: Session):
        return SystemService.get_settings(db)

    @staticmethod
    def update_settings(
        db: Session,
        system_name: str,
        logo,
        auto_logout_enabled: bool,
        auto_logout_time: int,
    ):
        return SystemService.update_settings(
            db,
            system_name,
            logo,
            auto_logout_enabled,
            auto_logout_time,
        )
