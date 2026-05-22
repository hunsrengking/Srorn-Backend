from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.constants.positions_constants import POSITIONS_STUDENT


class StudentRequest(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    khmer_firstname: str | None = None
    khmer_lastname: str | None = None
    position_id: int = POSITIONS_STUDENT
    is_active: bool = True
    is_deleted: bool = False
    

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
