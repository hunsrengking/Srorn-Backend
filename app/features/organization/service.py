from unittest import case

from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.config import db
from app.features.positions.schema import Position
from app.features.organization.print_card_schema import PrintCard, print_cards_mapping
from app.features.staff.schema import Staff
from app.features.students.schema import Student 
from sqlalchemy.orm import aliased, Session
from sqlalchemy import func
from app.features.staff.service import get_all_staff
from app.features.students.service import StudentService
from fastapi import BackgroundTasks
from app.features.notifications.service import notify_action
from app.config.iconfig import FRONTEND_URL
from app.features.organization.models import PrintCardUpdate
from app.features.users.schema import User

class OrganizationService:
    
    @staticmethod
    def getAllPrintCardTemplate(db):
        try:
            staffs = get_all_staff(db)
            students = StudentService.get_all_students(db)
            
            # Fetch positions
            positions = db.query(Position).filter(Position.is_active == True).all()

            # Map staff rows to dict for response
            staff_list = [dict(s._mapping) for s in staffs]

            return {
                "staffs": staff_list,
                "students": students,
                "positions": positions
            }

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

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
        EntryStaff = aliased(Staff)
        SellerStaff = aliased(Staff)
        StaffPosition = aliased(Position)
        StudentPosition = aliased(Position)

        try:
            # Query the card details with names and positions
            print_card = (
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
                .filter(PrintCard.id == print_card_id)
                .first()
            )

            if not print_card:
                raise HTTPException(
                    status_code=404,
                    detail="Print card not found"
                )

            # Fetch associated mappings
            mappings = db.query(print_cards_mapping).filter(print_cards_mapping.c.print_card_id == print_card_id).all()
            
            # Combine into a single dictionary
            result = dict(print_card._mapping)
            result["mappings"] = [dict(m._mapping) for m in mappings]
            
            return result

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )


    @staticmethod
    def PrintCardNew(print_card_data, db, current_user, background_tasks: BackgroundTasks):
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

            # ================= NOTIFICATION & TELEGRAM =================
            card_url = f"{FRONTEND_URL}/organization/printcard/views/{new_print_card.id}"
            telegram_msg = (
                f"<b>📇 New Print Card:</b> #{new_print_card.id}\n"
                f"<b>👤 Created by:</b> {current_user.username}\n"
                f"<b>📅 Date:</b> {new_print_card.print_date.strftime('%d %b %Y')}\n"
                f"<b>📝 Description:</b> {new_print_card.description or 'No description'}\n"
                "==============================\n"
                f'🔗 <a href="{card_url}">View Print Card</a>'
            )

            notify_action(
                db=db,
                user=current_user,
                title="New Print Card Created",
                message=f"Print Card #{new_print_card.id} has been created",
                link=f"/organization/printcard/views/{new_print_card.id}",
                notification_type="print_card",
                background_tasks=background_tasks,
                telegram_message=telegram_msg,
            )

            return new_print_card

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

    @staticmethod
    def UpdatePrintCard(print_card_id: int, print_card_data: PrintCardUpdate, db: Session, current_user: User, background_tasks: BackgroundTasks):
        try:
            # Fetch the print card
            print_card = db.query(PrintCard).filter(PrintCard.id == print_card_id).first()
            if not print_card:
                raise HTTPException(status_code=404, detail="Print card not found")

            # Update fields
            update_data = print_card_data.dict(exclude_unset=True)
            
            # Handle mappings update
            mappings_data = update_data.pop("mappings", None)
            
            for field, value in update_data.items():
                setattr(print_card, field, value)

            db.commit()
            db.refresh(print_card)

            # Update mappings if provided
            if mappings_data is not None:
                # Delete existing mappings
                db.execute(print_cards_mapping.delete().where(print_cards_mapping.c.print_card_id == print_card_id))
                
                # Insert new mappings
                for m in mappings_data:
                    mapping = print_cards_mapping.insert().values(
                        print_card_id=print_card.id,
                        cable_color_id=m["cable_color_id"],
                        quantity=m["quantity"]
                    )
                    db.execute(mapping)
                
                db.commit()

            # ================= NOTIFICATION & TELEGRAM =================
            card_url = f"{FRONTEND_URL}/organization/printcard/views/{print_card.id}"
            telegram_msg = (
                f"<b>✏️ Print Card Updated:</b> #{print_card.id}\n"
                f"<b>👤 Updated by:</b> {current_user.username}\n"
                f"<b>📅 Date:</b> {print_card.print_date.strftime('%d %b %Y')}\n"
                f"<b>📝 Description:</b> {print_card.description or 'No description'}\n"
                "==============================\n"
                f'🔗 <a href="{card_url}">View Print Card</a>'
            )

            notify_action(
                db=db,
                user=current_user,
                title="Print Card Updated",
                message=f"Print Card #{print_card.id} has been updated",
                link=f"/organization/printcard/views/{print_card.id}",
                notification_type="print_card",
                background_tasks=background_tasks,
                telegram_message=telegram_msg,
            )

            return print_card

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))