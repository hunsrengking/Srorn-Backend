from sqlalchemy.orm import Session
from app.schema.system_schema import SystemSettings
import os
import shutil
from fastapi import UploadFile

class SystemService:
    @staticmethod
    def get_settings(db: Session):
        settings = db.query(SystemSettings).first()
        if not settings:
            # Create default settings if not exists
            settings = SystemSettings(system_name="Support System", logo_url="/assets/images/logo/logo.PNG")
            db.add(settings)
            db.commit()
            db.refresh(settings)
        return settings

    @staticmethod
    def update_settings(db: Session, system_name: str, logo: UploadFile = None, auto_logout_enabled: bool = False, auto_logout_time: int = 30):
        settings = db.query(SystemSettings).first()
        if not settings:
            settings = SystemSettings(
                system_name=system_name,
                auto_logout_enabled=auto_logout_enabled,
                auto_logout_time=auto_logout_time
            )
            db.add(settings)
        else:
            settings.system_name = system_name
            settings.auto_logout_enabled = auto_logout_enabled
            settings.auto_logout_time = auto_logout_time

        if logo:
            # Simple file save logic
            upload_dir = "public/uploads/system"
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            file_path = os.path.join(upload_dir, logo.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(logo.file, buffer)
            
            # Save relative URL
            settings.logo_url = f"/uploads/system/{logo.filename}"

        db.commit()
        db.refresh(settings)
        return settings
