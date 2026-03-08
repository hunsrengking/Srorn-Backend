from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


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

    class Config:
        from_attributes = True

    class Config:
        from_attributes = True