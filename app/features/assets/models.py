from pydantic import BaseModel, field_validator
from app.features.setting.code.models import CodeValueResponse
from app.features.organization.offices.models import OfficeResponse
from app.features.organization.departments.models import DepartmentResponse
from datetime import datetime


class CodeValueMinResponse(BaseModel):
    id: int
    code_value: str
    code_description: str | None = None

    class Config:
        from_attributes = True


class AssetsTemplate(BaseModel):
    assetTypeOptions: list[CodeValueResponse]
    officeOptions: list[OfficeResponse]
    departmentOptions: list[DepartmentResponse]
    modelOptions: list[CodeValueResponse]
    cpuOptions: list[CodeValueResponse]
    ramOptions: list[CodeValueResponse]
    hhdOptions: list[CodeValueResponse]
    osOptions: list[CodeValueResponse]
    locationOptions: list[CodeValueResponse]

    class Config:
        from_attributes = True


class AssetRequest(BaseModel):
    device_type_id: int | None = None
    device_model_id: int | None = None
    device_name: str | None = None
    serial_number: str | None = None
    switch_port: str | None = None
    manufacturer: str | None = None
    size: str | None = None
    mac_address: str | None = None
    ip_address: str | None = None
    cpu_id: int | None = None
    ram_id: int | None = None
    hhd_id: int | None = None
    os_id: int | None = None
    part_upgrade: str | None = None
    location_id: int | None = None
    office_id: int | None = None
    department_id: int | None = None
    building_brand: str | None = None
    description: str | None = None
    image_url: str | None = None

    @field_validator(
        "device_type_id",
        "device_model_id",
        "cpu_id",
        "ram_id",
        "hhd_id",
        "os_id",
        "location_id",
        "office_id",
        "department_id",
        mode="before",
    )
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v


class AssetResponse(BaseModel):
    id: int
    device_type_id: int | None = None
    device_model_id: int | None = None
    device_name: str | None = None
    serial_number: str | None = None
    switch_port: str | None = None
    manufacturer: str | None = None
    size: str | None = None
    mac_address: str | None = None
    ip_address: str | None = None
    cpu_id: int | None = None
    ram_id: int | None = None
    hhd_id: int | None = None
    os_id: int | None = None
    part_upgrade: str | None = None
    location_id: int | None = None
    office_id: int | None = None
    department_id: int | None = None
    building_brand: str | None = None
    description: str | None = None
    image_url: str | None = None
    created_at: datetime | None = None

    # Nested relations
    device_type: CodeValueMinResponse | None = None
    device_model: CodeValueMinResponse | None = None
    location: CodeValueMinResponse | None = None
    department: DepartmentResponse | None = None
    cpu: CodeValueMinResponse | None = None
    ram: CodeValueMinResponse | None = None
    hhd: CodeValueMinResponse | None = None
    os: CodeValueMinResponse | None = None
    office: OfficeResponse | None = None
    user_name: str | None = None

    class Config:
        from_attributes = True
