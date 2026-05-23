from pydantic import BaseModel


class CodeRequest(BaseModel):
    codes_name: str
    is_active: bool = True


class CodeResponse(BaseModel):
    id: int
    codes_name: str
    is_active: bool

    class Config:
        from_attributes = True


class CodeValueRequest(BaseModel):
    code_id: int
    code_value: str
    code_description: str | None = None
    order_position: int
    is_active: bool = True


class CodeValueResponse(BaseModel):
    id: int
    code_id: int
    code_value: str
    code_description: str | None = None
    order_position: int
    is_active: bool

    class Config:
        from_attributes = True
