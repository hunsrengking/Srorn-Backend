from typing import Any

from pydantic import BaseModel, Field


class DepartmentRequest(BaseModel):
    name: str
    status_id: int = Field(default=1)
    description: str | None = None


class DepartmentResponse(BaseModel):
    id: int
    name: str
    status_id: int | None = None
    description: str | None = None
    members: list[dict[str, Any]] = Field(default_factory=list)

    class Config:
        from_attributes = True
