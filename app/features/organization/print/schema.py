from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.config.db import Base

print_cards_mapping = Table(
    "print_cards_mapping",
    Base.metadata,
    Column("print_card_id", Integer, ForeignKey("print_cards.id")),
    Column("cable_color_id", Integer, nullable=True),
    Column("quantity", Integer, nullable=False, default=1),
)


class PrintCard(Base):
    __tablename__ = "print_cards"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=True)
    print_date = Column(DateTime, nullable=False)
    is_print_card = Column(Boolean, default=True)
    seller_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    description = Column(String(255), nullable=True)

    seller = relationship(
        "Staff", foreign_keys=[seller_id], back_populates="print_cards"
    )
    student = relationship("Student", foreign_keys=[student_id])
    staff = relationship("Staff", foreign_keys=[staff_id])
