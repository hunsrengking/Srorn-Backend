from datetime import datetime
from pydantic import BaseModel, Field, computed_field


class StudentCreate(BaseModel):
    firstname: str
    lastname: str
    khmer_firstname: str | None
    khmer_lastname: str | None
    position_id: int | None
    is_active: bool
    created_at: datetime = Field(default_factory=datetime.now)
    is_deleted: bool


class StudentUpdate(BaseModel):
    firstname: str | None
    lastname: str | None
    khmer_firstname: str | None
    khmer_lastname: str | None
    position_id: int | None
    is_active: bool | None
    updated_at: datetime = Field(default_factory=datetime.now)
    is_deleted: bool | None


class StudentResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    khmer_firstname: str | None
    khmer_lastname: str | None
    position_id: int | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    @computed_field
    @property
    def display_name(self) -> str:
        return f"{self.firstname} {self.lastname}"

    class Config:
        from_attributes = True
