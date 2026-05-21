from sqlalchemy import Column, Integer, String,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from app.config.db import Base

class Code(Base):
    __tablename__ = "codes"
    id = Column(Integer, primary_key=True, index=True)
    codes_name = Column(String(50), nullable=False)
    is_active = Column(Boolean, nullable=False)

class CodeValue(Base):
    __tablename__ = "code_values"
    id = Column(Integer, primary_key=True, index=True)
    code_id = Column(Integer, ForeignKey("codes.id"))
    code_value = Column(String(50), nullable=False)
    code_description = Column(String(255), nullable=True)
    order_position = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)

    code = relationship("Code", back_populates="code_values")