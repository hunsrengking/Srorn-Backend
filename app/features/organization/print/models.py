from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class PrntCardMappingRequest(BaseModel):
    print_card_id: int | None = None
    cable_color_id: int | None = None
    quantity: int | None = None


class PrntCardMappingResponse(BaseModel):
    print_card_id: int | None = None
    cable_color_id: int | None = None
    quantity: int | None = None


class PrintCardRequest(BaseModel):
    student_id: int | None = None
    staff_id: int | None = None
    entry_id: int | None = None
    entity_type: str | None = None
    print_date: datetime | None = None
    is_print_card: bool | None = True
    seller_id: int | None = None
    description: str | None = None
    mappings: list[PrntCardMappingRequest] = Field(default_factory=list)


class PrintCardResponse(BaseModel):
    id: int
    student_id: int | None = None
    staff_id: int | None = None
    entry_id: int | None = None
    entity_type: str | None = None
    print_date: datetime | None = None
    is_print_card: bool | None = True
    seller_id: int | None = None
    description: str | None = None
    person_name: str | None = None
    seller_name: str | None = None
    mappings: list[PrntCardMappingResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True
