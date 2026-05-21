from sqlalchemy import Column, Integer, String, Boolean
from app.config.db import Base

class SystemSettings(Base):
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True)
    system_name = Column(String(255), nullable=False, default="Support System")
    logo_url = Column(String(255), nullable=True)
    auto_logout_enabled = Column(Boolean, default=False)
    auto_logout_time = Column(Integer, default=30)  # minutes
