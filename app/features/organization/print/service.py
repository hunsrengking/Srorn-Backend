from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased
from sqlalchemy import text
import datetime
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


class PrintCardService:

    @staticmethod
    def getPrintCardData(db):
        try:
            sql = text("""
                SELECT
                    pc.id,
                    s.id as student_id,
                    s.display_name as student_name,
                    pc.print_date as print_date,
                    pc.is_print_card as is_print_card,
                    teac.id as teacher_id,
                    teac.display_name as teacher_name,
                    sel.id as seller_id,
                    sel.display_name as seller_name,
                    pc.description
                FROM
                    print_cards pc
                LEFT JOIN students s ON pc.student_id = s.id
                LEFT JOIN staff teac ON pc.staff_id = teac.id
                LEFT JOIN staff sel ON pc.seller_id = sel.id
                GROUP BY 
                    pc.id,
                    s.id,
                    s.display_name,
                    pc.print_date,
                    pc.is_print_card,
                    teac.id,
                    teac.display_name,
                    sel.id,
                    sel.display_name,
                    pc.description
            """)

            results = db.execute(sql).fetchall()

            return [PrintCardService.PrintCardDataMapper(row) for row in results]

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )

    @staticmethod
    def getPrintCardMappingByCardId(print_card_id, db):
        try:
            sql = text("""
                SELECT
                    pcm.print_card_id,
                    pcm.cable_color_id,
                    pcm.quantity,
                    cc.code_value as cable_color_value
                FROM
                    print_cards_mapping pcm
                LEFT JOIN code_values cc ON pcm.cable_color_id = cc.id
                WHERE pcm.print_card_id = :print_card_id
            """)

            results = db.execute(sql, {"print_card_id": print_card_id}).fetchall()

            return [
                {
                    "print_card_id": row.print_card_id,
                    "cable_color_id": row.cable_color_id,
                    "quantity": row.quantity,
                    "cable_color_value": row.cable_color_value,
                }
                for row in results
            ]

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )

    @staticmethod
    def PrintCardDataMapper(
        row,
    ):
        student_id = row.student_id
        staff_id = row.staff_id
        entry_id = student_id if student_id is not None else staff_id
        entity_type = "student" if student_id is not None else "staff"

        return {
            "id": row.id,
            "student_id": student_id,
            "student_name": row.student_name,
            "print_date": row.print_date,
            "is_print_card": row.is_print_card,
            "staff_id": staff_id,
            "staff_name": row.staff_name,
            "seller_id": row.seller_id,
            "seller_name": row.seller_name,
            "description": row.description,
            "person_name": row.student_name or row.staff_name,
            "entry_id": entry_id,
            "entity_type": entity_type,
        }

    # ─────────────────────────────────────────────────────────────
    # Templates
    # ─────────────────────────────────────────────────────────────
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
    # Detail
    # ─────────────────────────────────────────────────────────────

    @staticmethod
    def getPrintCardById(print_card_id, db):

        try:
            sql = text("""
                SELECT
                    pc.id,
                    s.id as student_id,
                    s.display_name as student_name,
                    pc.print_date as print_date,
                    pc.is_print_card as is_print_card,
                    teac.id as staff_id,
                    teac.display_name as staff_name,
                    sel.id as seller_id,
                    sel.display_name as seller_name,
                    pc.description
                FROM
                    print_cards pc
                LEFT JOIN students s ON pc.student_id = s.id
                LEFT JOIN staff teac ON pc.staff_id = teac.id
                LEFT JOIN staff sel ON pc.seller_id = sel.id
                WHERE pc.id = :print_card_id
                LIMIT 1
            """)

            result = db.execute(sql, {"print_card_id": print_card_id}).fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Print card not found",
                )

            # Map to dictionary
            card_dict = PrintCardService.PrintCardDataMapper(result)

            # Load mappings
            card_dict["mappings"] = PrintCardService.getPrintCardMappingByCardId(
                print_card_id, db
            )

            return card_dict

        except HTTPException:
            raise

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )

    @staticmethod
    def getPrintCardByEntityId(entity_id, db):

        try:
            sql = text("""
                SELECT
                    pc.id,
                    s.id as student_id,
                    s.display_name as student_name,
                    pc.print_date as print_date,
                    pc.is_print_card as is_print_card,
                    teac.id as staff_id,
                    teac.display_name as staff_name,
                    sel.id as seller_id,
                    sel.display_name as seller_name,
                    pc.description
                FROM
                    print_cards pc
                LEFT JOIN students s ON pc.student_id = s.id
                LEFT JOIN staff teac ON pc.staff_id = teac.id
                LEFT JOIN staff sel ON pc.seller_id = sel.id
                WHERE student_id = :entity_id OR staff_id = :entity_id
                GROUP BY 
                    pc.id,
                    s.id,
                    s.display_name,
                    pc.print_date,
                    pc.is_print_card,
                    teac.id,
                    teac.display_name,
                    sel.id,
                    sel.display_name,
                    pc.description
            """)

            results = db.execute(sql, {"entity_id": entity_id}).fetchall()

            return [PrintCardService.PrintCardDataMapper(row) for row in results]

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

            student_id = print_card_data.student_id
            staff_id = print_card_data.staff_id

            if print_card_data.entry_id and print_card_data.entity_type:
                if print_card_data.entity_type == "student":
                    student_id = print_card_data.entry_id
                elif print_card_data.entity_type == "staff":
                    staff_id = print_card_data.entry_id

            if not student_id and not staff_id:
                raise HTTPException(
                    status_code=400,
                    detail="student_id or staff_id is required",
                )

            # Create card
            new_card = PrintCard(
                student_id=student_id,
                staff_id=staff_id,
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
                        cable_color_id=m.cable_color_id,
                        quantity=m.quantity,
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

            return PrintCardService.getPrintCardById(
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

            student_id = print_card_data.student_id
            staff_id = print_card_data.staff_id

            if print_card_data.entry_id and print_card_data.entity_type:
                if print_card_data.entity_type == "student":
                    student_id = print_card_data.entry_id
                elif print_card_data.entity_type == "staff":
                    staff_id = print_card_data.entry_id

            if not student_id and not staff_id:
                raise HTTPException(
                    status_code=400,
                    detail="student_id or staff_id is required",
                )

            # Update card
            card.student_id = student_id  # type: ignore
            card.staff_id = staff_id  # type: ignore
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
                        print_card_id=print_card_id,
                        cable_color_id=m.cable_color_id,
                        quantity=m.quantity,
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

            return PrintCardService.getPrintCardById(
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

    @staticmethod
    def getPrintCardStats(db: Session):
        try:

            # Get current year or the year of the latest print card
            current_year = datetime.date.today().year
            latest_card = db.execute(
                text("SELECT MAX(print_date) FROM print_cards")
            ).scalar()
            if latest_card:
                if isinstance(latest_card, str):
                    try:
                        latest_card = datetime.datetime.strptime(
                            latest_card[:19], "%Y-%m-%d %H:%M:%S"
                        )
                    except:
                        try:
                            latest_card = datetime.datetime.strptime(
                                latest_card[:10], "%Y-%m-%d"
                            )
                        except:
                            pass
                if hasattr(latest_card, "year"):
                    current_year = latest_card.year # type: ignore

            # 1. Fetch active colors from code_values for 'Cable Color'
            sql_colors = text("""
                SELECT cv.code_value 
                FROM code_values cv 
                JOIN codes c ON cv.code_id = c.id 
                WHERE c.codes_name = 'Cable Color' AND cv.is_active = 1
            """)
            res_colors = db.execute(sql_colors).fetchall()
            active_colors = [row.code_value for row in res_colors]

            # Initialize months map for all 12 months of the current year
            months_map = {}
            for m_idx in range(1, 13):
                ym = f"{current_year}-{m_idx:02d}"
                months_map[ym] = {
                    "month": ym,
                    "total_card": 0,
                    "Cable": [{"color": color, "total": 0} for color in active_colors],
                }

            # 2. Query Card counts per month
            sql_cards = text("""
                SELECT DATE_FORMAT(print_date, '%Y-%m') as ym, COUNT(id) as total_card 
                FROM print_cards 
                GROUP BY ym
            """)
            res_cards = db.execute(sql_cards).fetchall()
            for row in res_cards:
                ym = row.ym
                if ym in months_map:
                    months_map[ym]["total_card"] = int(row.total_card or 0)

            # 3. Query Cable counts per month joining mappings and code_values
            sql_cables = text("""
                SELECT 
                    DATE_FORMAT(pc.print_date, '%Y-%m') as ym, 
                    cv.code_value as color, 
                    SUM(pcm.quantity) as total
                FROM print_cards pc
                JOIN print_cards_mapping pcm ON pc.id = pcm.print_card_id
                JOIN code_values cv ON pcm.cable_color_id = cv.id
                JOIN codes c ON cv.code_id = c.id
                WHERE c.codes_name = 'Cable Color'
                GROUP BY ym, color
            """)
            res_cables = db.execute(sql_cables).fetchall()
            for row in res_cables:
                ym = row.ym
                if ym in months_map:
                    found = False
                    for c in months_map[ym]["Cable"]:
                        if c["color"].lower() == row.color.lower():
                            c["total"] = int(row.total or 0)
                            found = True
                            break
                    if not found:
                        months_map[ym]["Cable"].append(
                            {"color": row.color, "total": int(row.total or 0)}
                        )

            # Sort stats by month key ascending
            sorted_stats = [months_map[k] for k in sorted(months_map.keys())]

            return sorted_stats

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )
