from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.db import Base
from app.features.organization.offices.schema import Office


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    device_type_id = Column(Integer, ForeignKey("code_values.id"))
    device_model_id = Column(Integer, ForeignKey("code_values.id"))
    device_name = Column(String(100), nullable=True)
    serial_number = Column(String(100), nullable=True)
    switch_port = Column(String(50), nullable=True)
    manufacturer = Column(String(100), nullable=True)
    size = Column(String(50), nullable=True)
    mac_address = Column(String(50), nullable=True)
    ip_address = Column(String(50), nullable=True)
    cpu_id = Column(Integer, ForeignKey("code_values.id"))
    ram_id = Column(Integer, ForeignKey("code_values.id"))
    hhd_id = Column(Integer, ForeignKey("code_values.id"))
    os_id = Column(Integer, ForeignKey("code_values.id"))
    part_upgrade = Column(String(100), nullable=True)
    location_id = Column(Integer, ForeignKey("code_values.id"))
    office_id = Column(Integer, ForeignKey("office.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    building_brand = Column(String(100), nullable=True)
    description = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)

    # Tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    device_type = relationship("CodeValue", foreign_keys=[device_type_id])
    device_model = relationship("CodeValue", foreign_keys=[device_model_id])
    location = relationship("CodeValue", foreign_keys=[location_id])
    department = relationship("Department")
    cpu = relationship("CodeValue", foreign_keys=[cpu_id])
    ram = relationship("CodeValue", foreign_keys=[ram_id])
    hhd = relationship("CodeValue", foreign_keys=[hhd_id])
    os = relationship("CodeValue", foreign_keys=[os_id])
    office = relationship("Office", foreign_keys=[office_id])
