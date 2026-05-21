from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, computed_field
from app.constants.positions_constants import POSITIONS_STUDENT


class StudentCreate(BaseModel):
    firstname: str
    lastname: str
    khmer_firstname: str | None = None
    khmer_lastname: str | None = None
    position_id: int = POSITIONS_STUDENT
    is_active: bool
    created_at: datetime = Field(default_factory=datetime.now)
    is_deleted: bool = False


class StudentUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    khmer_firstname: str | None = None
    khmer_lastname: str | None = None
    is_active: bool | None = None
    updated_at: datetime = Field(default_factory=datetime.now)
    is_deleted: bool | None = None
    
class StudentResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    khmer_firstname: str | None
    khmer_lastname: str | None
    display_name : str | None
    position_id: int | None
    position_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True
