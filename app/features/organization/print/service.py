from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, or_

from app.config.iconfig import FRONTEND_URL
from app.features.setting.code.service import CodeService
from app.features.notifications.service import NotificationService
from app.features.organization.print.models import PrintCardRequest
from app.features.organization.print.schema import (
    PrintCard,
    print_cards_mapping,
)
from app.features.organization.positions.schema import Position
from app.features.organization.staff.schema import Staff
from app.features.organization.staff.service import StaffService
from app.features.students.schema import Student
from app.features.students.service import StudentService


class OrganizationService:

    # ─────────────────────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────────────────────

    @staticmethod
    def print_card(db):

        EntryStaff = aliased(Staff)
        SellerStaff = aliased(Staff)
        StaffPosition = aliased(Position)
        StudentPosition = aliased(Position)

        return (
            db.query(
                PrintCard.id,
                func.coalesce(
                    PrintCard.staff_id,
                    PrintCard.student_id,
                ).label("entry_id"),
                func.coalesce(
                    EntryStaff.display_name,
                    Student.display_name,
                ).label("person_name"),
                func.coalesce(
                    StaffPosition.title,
                    StudentPosition.title,
                ).label("position_name"),
                PrintCard.print_date,
                PrintCard.is_print_card,
                PrintCard.seller_id,
                SellerStaff.display_name.label("seller_name"),
                PrintCard.description,
                func.if_(
                    PrintCard.staff_id != None,
                    "staff",
                    "student",
                ).label("entity_type"),
            )
            .outerjoin(
                EntryStaff,
                EntryStaff.id == PrintCard.staff_id,
            )
            .outerjoin(
                Student,
                Student.id == PrintCard.student_id,
            )
            .outerjoin(
                StaffPosition,
                StaffPosition.id == EntryStaff.position_id,
            )
            .outerjoin(
                StudentPosition,
                StudentPosition.id == Student.position_id,
            )
            .outerjoin(
                SellerStaff,
                SellerStaff.id == PrintCard.seller_id,
            )
        )

    # ─────────────────────────────────────────────────────────────
    # Templates
    # ─────────────────────────────────────────────────────────────

    @staticmethod
    def getAllPrintCardTemplate(db):

        try:

            staffs = [dict(s._mapping) for s in StaffService.get_all_staff(db)]

            students = StudentService.get_all_students(db)

            colors = [
                {
                    "id": c.id,
                    "code_value": c.code_value,
                    "code_description": c.code_description,
                }
                for c in CodeService.getCodeValueByCode(
                    "Cable Color",
                    db,
                )
            ]

            positions = db.query(Position).filter(Position.is_active == True).all()

            return {
                "staffs": staffs,
                "students": students,
                "positions": [
                    {
                        "id": p.id,
                        "title": p.title,
                    }
                    for p in positions
                ],
                "card_colors": colors,
            }

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )

    @staticmethod
    def getPrintCardStudentTemplate(entity_id, db):

        try:

            studentsOption = StudentService.get_student_by_id(
                entity_id,
                db,
            )

            cardColorsOption = [
                {
                    "id": c.id,
                    "code_value": c.code_value,
                    "code_description": c.code_description,
                }
                for c in CodeService.getCodeValueByCode(
                    "Cable Color",
                    db,
                )
            ]

            sellerOption = [
                dict(row._mapping) for row in StaffService.get_all_staff(db)
            ]

            return {
                "studentsOption": studentsOption,
                "cardColorsOption": cardColorsOption,
                "sellerOption": sellerOption,
            }

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )

    @staticmethod
    def getPrintCardStaffTemplate(entity_id, db):

        try:

            staff = StaffService.get_staff_by_id(
                entity_id,
                db,
            )

            staffsOption = {
                "id": staff.id,
                "display_name": staff.display_name,
                "firstname": staff.firstname,
                "lastname": staff.lastname,
                "position_id": staff.position_id,
                "is_active": staff.is_active,
            }

            cardColorsOption = [
                {
                    "id": c.id,
                    "code_value": c.code_value,
                    "code_description": c.code_description,
                }
                for c in CodeService.getCodeValueByCode(
                    "Cable Color",
                    db,
                )
            ]

            sellerOption = [
                dict(row._mapping) for row in StaffService.get_all_staff(db)
            ]

            return {
                "staffsOption": staffsOption,
                "cardColorsOption": cardColorsOption,
                "sellerOption": sellerOption,
            }

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )

    # ─────────────────────────────────────────────────────────────
    # List
    # ─────────────────────────────────────────────────────────────

    @staticmethod
    def getAllPrintCard(
        db,
        entry_id: int = None,  # type: ignore
        entity_type: str = None,  # type: ignore
    ):

        try:

            query = OrganizationService.print_card(db)

            if entry_id is not None:

                if entity_type == "student":

                    query = query.filter(PrintCard.student_id == entry_id)

                elif entity_type == "staff":

                    query = query.filter(PrintCard.staff_id == entry_id)

                else:

                    query = query.filter(
                        or_(
                            PrintCard.student_id == entry_id,
                            PrintCard.staff_id == entry_id,
                        )
                    )

            elif entity_type == "student":

                query = query.filter(PrintCard.student_id != None)

            elif entity_type == "staff":

                query = query.filter(PrintCard.staff_id != None)

            rows = query.order_by(PrintCard.id.desc()).all()

            return [dict(r._mapping) for r in rows]

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )

    # ─────────────────────────────────────────────────────────────
    # Detail
    # ─────────────────────────────────────────────────────────────

    @staticmethod
    def getAllPrintCardById(print_card_id, db):

        try:

            print_card = (
                OrganizationService.print_card(db)
                .filter(PrintCard.id == print_card_id)
                .first()
            )

            if not print_card:
                raise HTTPException(
                    status_code=404,
                    detail="Print card not found",
                )

            mappings = (
                db.query(print_cards_mapping)
                .filter(print_cards_mapping.c.print_card_id == print_card_id)
                .all()
            )

            result = dict(print_card._mapping)

            result["mappings"] = [dict(m._mapping) for m in mappings]

            return result

        except HTTPException:
            raise

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )

    # ─────────────────────────────────────────────────────────────
    # Create
    # ─────────────────────────────────────────────────────────────

    @staticmethod
    def PrintCardNew(
        print_card_data: PrintCardRequest,
        db: Session,
        current_user,
        background_tasks: BackgroundTasks,
    ):

        try:

            # Validate
            if not print_card_data.print_date:
                raise HTTPException(
                    status_code=400,
                    detail="print_date is required",
                )

            if not print_card_data.seller_id:
                raise HTTPException(
                    status_code=400,
                    detail="seller_id is required",
                )

            if not print_card_data.student_id and not print_card_data.staff_id:
                raise HTTPException(
                    status_code=400,
                    detail="student_id or staff_id is required",
                )

            # Create card
            new_card = PrintCard(
                student_id=print_card_data.student_id,
                staff_id=print_card_data.staff_id,
                print_date=print_card_data.print_date,
                is_print_card=print_card_data.is_print_card,
                seller_id=print_card_data.seller_id,
                description=print_card_data.description,
            )

            db.add(new_card)
            db.commit()
            db.refresh(new_card)

            # Save mappings
            for m in print_card_data.mappings:

                db.execute(
                    print_cards_mapping.insert().values(
                        print_card_id=new_card.id,
                        cable_color_id=m.get("cable_color_id"),
                        quantity=m.get("quantity", 1),
                    )
                )

            db.commit()

            # Notification
            card_url = f"{FRONTEND_URL}/organization/printcard/" f"{new_card.id}"

            telegram_msg = (
                f"<b>📇 New Print Card:</b> "
                f"#{new_card.id}\n"
                f"<b>👤 Created by:</b> "
                f"{current_user.username}\n"
                f"<b>📅 Date:</b> "
                f"{new_card.print_date.strftime('%d %b %Y')}\n"
                f"<b>📝 Description:</b> "
                f"{new_card.description or 'No description'}\n"
                "==============================\n"
                f'🔗 <a href="{card_url}">'
                f"View Print Card</a>"
            )

            NotificationService.notify_action(
                db=db,
                user=current_user,
                title="New Print Card Created",
                message=(f"Print Card #{new_card.id} " f"has been created"),
                link=f"/organization/printcard/{new_card.id}",
                notification_type="print_card",
                background_tasks=background_tasks,
                telegram_message=telegram_msg,
            )

            return OrganizationService.getAllPrintCardById(
                new_card.id,
                db,
            )

        except HTTPException:
            raise

        except Exception as e:

            db.rollback()

            raise HTTPException(
                status_code=500,
                detail=str(e),
            )

    # ─────────────────────────────────────────────────────────────
    # Update
    # ─────────────────────────────────────────────────────────────

    @staticmethod
    def UpdatePrintCard(
        print_card_id: int,
        print_card_data: PrintCardRequest,
        db: Session,
        current_user,
        background_tasks: BackgroundTasks,
    ):

        try:

            card = db.query(PrintCard).filter(PrintCard.id == print_card_id).first()

            if not card:
                raise HTTPException(
                    status_code=404,
                    detail="Print card not found",
                )

            # Validate
            if not print_card_data.print_date:
                raise HTTPException(
                    status_code=400,
                    detail="print_date is required",
                )

            if not print_card_data.seller_id:
                raise HTTPException(
                    status_code=400,
                    detail="seller_id is required",
                )

            if not print_card_data.student_id and not print_card_data.staff_id:
                raise HTTPException(
                    status_code=400,
                    detail="student_id or staff_id is required",
                )

            # Update card
            card.student_id = print_card_data.student_id  # type: ignore
            card.staff_id = print_card_data.staff_id  # type: ignore
            card.print_date = print_card_data.print_date  # type: ignore
            card.is_print_card = print_card_data.is_print_card  # type: ignore
            card.seller_id = print_card_data.seller_id  # type: ignore
            card.description = print_card_data.description  # type: ignore

            db.commit()
            db.refresh(card)

            # Delete old mappings
            db.execute(
                print_cards_mapping.delete().where(
                    print_cards_mapping.c.print_card_id == print_card_id
                )
            )

            # Insert new mappings
            for m in print_card_data.mappings:

                db.execute(
                    print_cards_mapping.insert().values(
                        print_card_id=card.id,
                        cable_color_id=m.get("cable_color_id"),
                        quantity=m.get("quantity", 1),
                    )
                )

            db.commit()

            # Notification
            card_url = f"{FRONTEND_URL}/organization/printcard/" f"{card.id}"

            telegram_msg = (
                f"<b>✏️ Print Card Updated:</b> "
                f"#{card.id}\n"
                f"<b>👤 Updated by:</b> "
                f"{current_user.username}\n"
                f"<b>📅 Date:</b> "
                f"{card.print_date.strftime('%d %b %Y')}\n"
                f"<b>📝 Description:</b> "
                f"{card.description or 'No description'}\n"
                "==============================\n"
                f'🔗 <a href="{card_url}">'
                f"View Print Card</a>"
            )

            NotificationService.notify_action(
                db=db,
                user=current_user,
                title="Print Card Updated",
                message=(f"Print Card #{card.id} " f"has been updated"),
                link=f"/organization/printcard/{card.id}",
                notification_type="print_card",
                background_tasks=background_tasks,
                telegram_message=telegram_msg,
            )

            return OrganizationService.getAllPrintCardById(
                card.id,
                db,
            )

        except HTTPException:
            raise

        except Exception as e:

            db.rollback()

            raise HTTPException(
                status_code=500,
                detail=str(e),
            )
