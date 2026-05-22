from datetime import date
from typing import Optional

from pydantic import BaseModel


class StaffRequest(BaseModel):
    external_id: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    display_name: Optional[str] = None
    mobile_no: Optional[str] = None
    join_on_date: Optional[date] = None
    position_id: Optional[int] = None
    is_active: Optional[bool] = True


class StaffResponse(BaseModel):
    id: int
    external_id: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]
    display_name: Optional[str]
    mobile_no: Optional[str]
    join_on_date: Optional[date]
    position_id: Optional[int]
    position_title: Optional[str]
    is_active: bool
