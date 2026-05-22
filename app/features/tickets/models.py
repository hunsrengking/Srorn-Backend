from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class TicketRequest(BaseModel):
    title: str | None = None
    description: Optional[str] = None
    status_id: Optional[int] = None
    priority_id: Optional[int] = None
    category_id: Optional[int] = None
    assigned_to_id: Optional[int] = None
    assigned_to_department_id: Optional[int] = None
    approved_by_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    items: Optional[list[dict[str, Any]]] = None


class TicketResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status_id: int
    status_name: Optional[str] = None
    priority_id: Optional[int] = None
    priority_name: Optional[str] = None
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    assigned_to_id: Optional[int] = None
    assigned_to_name: Optional[str] = None
    assigned_to_department_id: Optional[int] = None
    assigned_by_id: Optional[int] = None
    approved_by_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    create_date: Optional[datetime] = None
    approved_date: Optional[datetime] = None
    items: list[dict[str, Any]] = Field(default_factory=list)

    class Config:
        from_attributes = True
