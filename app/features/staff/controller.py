from sqlalchemy.orm import Session

from app.features.staff import service as staff_service
from app.features.staff.models import StaffCreate, StaffUpdate


class StaffController:
    @staticmethod
    def _to_response(staff):
        position_title = getattr(staff, "position_title", None)
        position = getattr(staff, "position", None)
        if position_title is None and position:
            position_title = position.title

        return {
            "id": staff.id,
            "external_id": staff.external_id,
            "firstname": staff.firstname,
            "lastname": staff.lastname,
            "display_name": staff.display_name,
            "mobile_no": staff.mobile_no,
            "join_on_date": staff.join_on_date,
            "is_active": staff.is_active,
            "position_id": staff.position_id,
            "position_title": position_title,
        }

    @staticmethod
    def get_all(db: Session):
        rows = staff_service.get_all_staff(db)
        return [StaffController._to_response(row) for row in rows]

    @staticmethod
    def get_by_id(staff_id: int, db: Session):
        staff = staff_service.get_staff_by_id(staff_id, db)
        return StaffController._to_response(staff)

    @staticmethod
    def create(data: StaffCreate, db: Session, current_user, background_tasks):
        staff = staff_service.create_staff(data, db, current_user, background_tasks)
        return StaffController._to_response(staff)

    @staticmethod
    def update(staff_id: int, data: StaffUpdate, db: Session):
        staff = staff_service.update_staff(staff_id, data, db)
        return StaffController._to_response(staff)

    @staticmethod
    def delete(staff_id: int, db: Session):
        return staff_service.delete_staff(staff_id, db)
