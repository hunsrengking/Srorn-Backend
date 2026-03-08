from unittest import case

from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.config import db
from app.schema.position_schema import Position
from app.schema.print_card_schema import PrintCard,print_cards_mapping
from app.schema.staff_schema import Staff
from app.schema.student_schema import Student 
from sqlalchemy.orm import aliased
from sqlalchemy import func

class OrganizationService:
    
    @staticmethod
    def getAllPrintCard(db):
        EntryStaff = aliased(Staff)
        SellerStaff = aliased(Staff)
        StaffPosition = aliased(Position)
        StudentPosition = aliased(Position)

        try:
            print_cards = (
                db.query(
                    PrintCard.id,
                    PrintCard.entry_id,
                    func.coalesce(EntryStaff.display_name, Student.display_name).label("person_name"),
                    func.coalesce(StaffPosition.title, StudentPosition.title).label("position_name"),
                    PrintCard.print_date,
                    PrintCard.is_print_card,
                    PrintCard.seller_id,
                    SellerStaff.display_name.label("seller_name"),
                    PrintCard.description
                )
                .outerjoin(EntryStaff, EntryStaff.id == PrintCard.entry_id)
                .outerjoin(Student, Student.id == PrintCard.entry_id)
                .outerjoin(StaffPosition, StaffPosition.id == EntryStaff.position_id)
                .outerjoin(StudentPosition, StudentPosition.id == Student.position_id)
                .outerjoin(SellerStaff, SellerStaff.id == PrintCard.seller_id)
                .all()
            )

            return print_cards

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
            
    @staticmethod
    def getAllPrintCardById(print_card_id, db):
        try:
            print_card = db.query(PrintCard).filter(PrintCard.id == print_card_id).first()
            return print_card
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )


    @staticmethod
    def PrintCardNew(print_card_data, db):
        try:
            data = print_card_data.dict()
            mappings = data.pop("mappings", [])

            new_print_card = PrintCard(**data)
            db.add(new_print_card)
            db.commit()
            db.refresh(new_print_card)

            for m in mappings:
                mapping = print_cards_mapping.insert().values(
                    print_card_id=new_print_card.id,
                    cable_color_id=m["cable_color_id"],
                    quantity=m["quantity"]
                )
                db.execute(mapping)

            db.commit()

            return new_print_card

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )