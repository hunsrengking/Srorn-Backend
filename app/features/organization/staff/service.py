from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session

from app.features.notifications.service import NotificationService
from app.features.organization.positions.schema import Position
from app.features.organization.staff.models import StaffRequest
from app.features.organization.staff.schema import Staff


class StaffService:
    @staticmethod
    def get_all_staff(db: Session):
        return (
            db.query(
                Staff.id,
                Staff.external_id,
                Staff.firstname,
                Staff.lastname,
                Staff.display_name,
                Staff.mobile_no,
                Staff.join_on_date,
                Staff.is_active,
                Staff.position_id,
                Position.title.label("position_title"),
            )
            .outerjoin(Position, Staff.position_id == Position.id)
            .order_by(Staff.id.desc())
            .all()
        )

    @staticmethod
    def get_staff_by_id(staff_id: int, db: Session) -> Staff:
        staff = db.query(Staff).filter(Staff.id == staff_id).first()

        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff not found",
            )

        return staff

    @staticmethod
    def create_staff(
        data: StaffRequest,
        db: Session,
        current_user=None,
        background_tasks: BackgroundTasks | None = None,
    ):
        display_name = data.display_name or f"{data.firstname or ''} {data.lastname or ''}".strip()

        staff = Staff(
            external_id=data.external_id,
            firstname=data.firstname,
            lastname=data.lastname,
            display_name=display_name,
            mobile_no=data.mobile_no,
            join_on_date=data.join_on_date,
            position_id=data.position_id,
            is_active=data.is_active,
        )

        db.add(staff)
        db.commit()
        db.refresh(staff)

        if current_user and background_tasks:
            telegram_msg = (
                f"<b>New Staff Created:</b> {staff.display_name}\n"
                f"<b>External ID:</b> {staff.external_id}\n"
                f"<b>Mobile:</b> {staff.mobile_no}\n"
                f"<b>Created by:</b> {current_user.username}\n"
                "==============================\n"
            )
            NotificationService.notify_action(
                db=db,
                user=current_user,
                title="New Staff Created",
                message=f"Staff {staff.display_name} has been added",
                link=f"/staff/views/{staff.id}",
                notification_type="staff",
                background_tasks=background_tasks,
                telegram_message=telegram_msg,
            )

        return staff

    @staticmethod
    def update_staff(staff_id: int, data: StaffRequest, db: Session):
        staff = StaffService.get_staff_by_id(staff_id, db)

        for key, value in data.dict(exclude_unset=True).items():
            setattr(staff, key, value)

        if data.firstname is not None or data.lastname is not None:
            staff.display_name = f"{staff.firstname or ''} {staff.lastname or ''}".strip()  # type: ignore

        db.commit()
        db.refresh(staff)
        return staff

    @staticmethod
    def delete_staff(staff_id: int, db: Session):
        staff = StaffService.get_staff_by_id(staff_id, db)
        db.delete(staff)
        db.commit()
        return {"message": "Staff deleted successfully"}
