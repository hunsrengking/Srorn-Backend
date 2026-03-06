from sqlalchemy import Boolean, Column, Date, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.config.db import Base


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(255), nullable=True)
    lastname = Column(String(255), nullable=True)
    display_name = Column(String(255), nullable=True)
    khmer_firstname = Column(String(255), nullable=True)
    khmer_lastname = Column(String(255), nullable=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)


    # Relationships
    position = relationship("Position", back_populates="students")