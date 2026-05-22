from pydantic import BaseModel, Field


class RoleRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    permissions: list[int] = Field(default_factory=list)


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    permissions: list[dict] = Field(default_factory=list)
