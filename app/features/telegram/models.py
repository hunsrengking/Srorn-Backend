from typing import Optional

from pydantic import BaseModel


class TelegramConfigRequest(BaseModel):
    bot_token: str | None = None
    chat_id: str | None = None
    is_active: Optional[bool] = None


class TelegramConfigResponse(BaseModel):
    id: int
    bot_token: str
    chat_id: str
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True
