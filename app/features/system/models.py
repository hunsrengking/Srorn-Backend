from typing import Optional
from pydantic import BaseModel

class SystemSettingsBase(BaseModel):
    system_name: str
    logo_url: Optional[str] = None
    auto_logout_enabled: bool = False
    auto_logout_time: int = 30  # minutes

class SystemSettingsResponse(SystemSettingsBase):
    id: int

    class Config:
        from_attributes = True
