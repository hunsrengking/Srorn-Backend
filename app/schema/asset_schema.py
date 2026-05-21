from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.db import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    device_name = Column(String(100), nullable=True)
    device_serial_number = Column(String(100), nullable=True)
    device_description = Column(String(255), nullable=True)
    device_image = Column(String(255), nullable=True)

    # Relations
    device_type_id = Column(Integer, ForeignKey("device_types.id"))
    device_model_id = Column(Integer, ForeignKey("device_models.id"))
    device_status_id = Column(Integer, ForeignKey("device_statuses.id"))
    device_location_id = Column(Integer, ForeignKey("device_locations.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))

    # Network Info
    mac_address = Column(String(50), nullable=True)
    ip_address = Column(String(50), nullable=True)

    # Hardware Info
    cpu = Column(String(100), nullable=True)
    ram = Column(String(50), nullable=True)
    storage = Column(String(50), nullable=True)
    os = Column(String(50), nullable=True)

    # Tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    device_type = relationship("DeviceType")
    device_model = relationship("DeviceModels")
    device_status = relationship("DeviceStatus")
    device_location = relationship("DeviceLocation")
    department = relationship("Department")