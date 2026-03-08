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
    entry_id = Column(Integer, nullable=False)
    print_date = Column(DateTime, nullable=False)
    is_print_card = Column(Boolean, default=True)

    # FIX HERE
    seller_id = Column(Integer, ForeignKey("staff.id"), nullable=False)

    description = Column(String(255), nullable=True)

    seller = relationship("Staff", back_populates="print_cards")