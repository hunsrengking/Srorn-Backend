from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class PrintCardRequest(BaseModel):
    entry_id: int | None = None
    print_date: datetime | None = None
    is_print_card: bool | None = True
    seller_id: int | None = None
    description: str | None = None
    mappings: list[dict[str, Any]] = Field(default_factory=list)


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
    mappings: list[dict[str, Any]] = Field(default_factory=list)

    class Config:
        from_attributes = True
