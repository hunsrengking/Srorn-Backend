from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class PositionRequest(BaseModel):
    title: str | None = None
    level: Optional[str] = None
    min_salary: Optional[Decimal] = None
    max_salary: Optional[Decimal] = None
    is_active: Optional[bool] = True


class PositionResponse(BaseModel):
    id: int
    title: str
    level: Optional[str] = None
    min_salary: Optional[Decimal] = None
    max_salary: Optional[Decimal] = None
    is_active: Optional[bool] = True
    created_at: datetime

    class Config:
        from_attributes = True
