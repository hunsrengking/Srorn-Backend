from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.db import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)

    # Relations
    device_type_id = Column(Integer, ForeignKey("device_types.id"))
    device_model_id = Column(Integer, ForeignKey("device_models.id"))
    status_id = Column(Integer, ForeignKey("code_values.id"))
    location_id = Column(Integer, ForeignKey("code_values.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))

    # Network Info
    mac_address = Column(String(50), nullable=True)
    ip_address = Column(String(50), nullable=True)

    # Hardware Info
    cpu_id = Column(Integer, ForeignKey("code_values.id"))
    ram_id = Column(Integer, ForeignKey("code_values.id"))
    storage_id = Column(Integer, ForeignKey("code_values.id"))
    os_id = Column(Integer, ForeignKey("code_values.id"))

    # Tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    device_type = relationship("DeviceType")
    device_model = relationship("DeviceModels")
    status = relationship("CodeValue", foreign_keys=[status_id])
    location = relationship("CodeValue", foreign_keys=[location_id])
    department = relationship("Department")
    cpu = relationship("CodeValue", foreign_keys=[cpu_id])
    ram = relationship("CodeValue", foreign_keys=[ram_id])
    storage = relationship("CodeValue", foreign_keys=[storage_id])
    os = relationship("CodeValue", foreign_keys=[os_id])