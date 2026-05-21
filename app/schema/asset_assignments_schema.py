from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.db import Base

class AssetAssignment(Base):
    __tablename__ = "asset_assignments"

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    staff_id = Column(Integer, ForeignKey("staffs.id"))
    assigned_date = Column(DateTime, default=func.now())
    returned_date = Column(DateTime, nullable=True)

    asset = relationship("Asset")
    staff = relationship("Staff")