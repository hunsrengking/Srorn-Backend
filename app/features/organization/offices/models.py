from datetime import datetime
from pydantic import BaseModel


class OfficeRequest(BaseModel):
    external_id: str | None = None
    name: str | None = None
    is_active: bool | None = None
    is_delete: bool | None = None


class OfficeResponse(BaseModel):
    id: int
    external_id: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    is_delete: bool

    class Config:
        from_attributes = True
