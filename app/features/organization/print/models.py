from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class PrintCardRequest(BaseModel):
    student_id: int | None = None
    staff_id: int | None = None
    print_date: datetime | None = None
    is_print_card: bool | None = True
    seller_id: int | None = None
    description: str | None = None
    mappings: list[dict[str, Any]] = Field(default_factory=list)


class PrintCardResponse(BaseModel):
    id: int
    student_id: int | None = None
    staff_id: int | None = None
    print_date: datetime | None = None
    is_print_card: bool | None = True
    seller_id: int | None = None
    description: str | None = None
    mappings: list[dict[str, Any]] = Field(default_factory=list)

    class Config:
        from_attributes = True
