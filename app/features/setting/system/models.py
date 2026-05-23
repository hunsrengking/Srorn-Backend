from typing import Optional

from pydantic import BaseModel


class SystemSettingsRequest(BaseModel):
    system_name: str
    logo_url: Optional[str] = None
    auto_logout_enabled: bool = False
    auto_logout_time: int = 30


class SystemSettingsResponse(BaseModel):
    id: int
    system_name: str
    logo_url: Optional[str] = None
    auto_logout_enabled: bool = False
    auto_logout_time: int = 30

    class Config:
        from_attributes = True
