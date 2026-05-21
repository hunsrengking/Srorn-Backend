from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.staff_model import StaffResponse
from app.models.student_model import StudentResponse
from app.models.positions_model import PositionResponse



class PrintCardMapping(BaseModel):
    print_card_id: int | None = None
    cable_color_id: Optional[int] = None
    quantity: int = Field(default=1, gt=0)

    class Config:
        from_attributes = True


class PrintCardCreate(BaseModel):
    entry_id: int
    print_date: datetime
    is_print_card: bool
    seller_id: int
    description: str | None
    mappings: List[PrintCardMapping] = []

class PrintCardUpdate(BaseModel):
    entry_id: Optional[int] = None
    print_date: Optional[datetime] = None
    is_print_card: Optional[bool] = None
    seller_id: Optional[int] = None
    description: Optional[str] = None
    mappings: Optional[List[PrintCardMapping]] = None

class PrintCardTemplate(BaseModel):
    staffs: List[StaffResponse]
    students: List[StudentResponse]
    positions: List[PositionResponse]


class PrintCardResponse(BaseModel):
    id: int
    entry_id: int
    person_name: Optional[str] = None
    position_name: Optional[str] = None
    print_date: datetime
    is_print_card: bool
    seller_id: int
    seller_name: Optional[str] = None
    description: Optional[str] = None
    mappings: List[PrintCardMapping] = []

    class Config:
        from_attributes = True