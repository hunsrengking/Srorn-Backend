from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.db import Base

class DeviceType(Base):
    __tablename__ = "device_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)

    assets = relationship("Asset", back_populates="device_type")
    device_models = relationship("DeviceModel", back_populates="device_type")