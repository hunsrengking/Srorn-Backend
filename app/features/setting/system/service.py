import os

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.config.cloudinary import upload_image_to_cloudinary
from app.features.setting.system.schema import SystemSettings


class SystemService:
    @staticmethod
    def _is_missing_local_logo(logo_url: str | None) -> bool:
        if not logo_url:
            return False

        if logo_url.startswith("/api/uploads/"):
            local_path = logo_url.replace("/api/uploads/", "public/uploads/", 1)
            return not os.path.exists(local_path)

        if logo_url.startswith("/uploads/"):
            local_path = logo_url.replace("/uploads/", "public/uploads/", 1)
            return not os.path.exists(local_path)

        return False

    @staticmethod
    def get_settings(db: Session):
        settings = db.query(SystemSettings).first()
        if not settings:
            # Create default settings if not exists
            settings = SystemSettings(
                system_name="Support System", logo_url="/assets/images/logo/logo.PNG"
            )
            db.add(settings)
            db.commit()
            db.refresh(settings)
        elif SystemService._is_missing_local_logo(settings.logo_url):  # type: ignore
            settings.logo_url = None  # type: ignore
            db.commit()
            db.refresh(settings)
        return settings

    @staticmethod
    def update_settings(db: Session, system_name: str, logo: UploadFile = None, auto_logout_enabled: bool = False, auto_logout_time: int = 30):  # type: ignore
        settings = db.query(SystemSettings).first()
        if not settings:
            settings = SystemSettings(
                system_name=system_name,
                auto_logout_enabled=auto_logout_enabled,
                auto_logout_time=auto_logout_time,
            )
            db.add(settings)
        else:
            settings.system_name = system_name  # type: ignore
            settings.auto_logout_enabled = auto_logout_enabled  # type: ignore
            settings.auto_logout_time = auto_logout_time  # type: ignore

        if logo:
            settings.logo_url = upload_image_to_cloudinary(logo)  # type: ignore

        db.commit()
        db.refresh(settings)
        return settings
