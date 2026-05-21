from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, computed_field


class OfficeCreate(BaseModel):
    external_id: str
    name: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    is_delete: bool = False

class OfficeUpdate(BaseModel):
    external_id: str | None = None
    name: str | None = None
    is_active: bool | None = None
    updated_at: datetime = Field(default_factory=datetime.now)
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
