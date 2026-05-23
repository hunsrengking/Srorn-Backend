from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, BackgroundTasks
from app.features.organization.offices.schema import Office
from app.features.notifications.service import NotificationService


class OfficeService:

    @staticmethod
    def created(office_data, db, current_user=None, background_tasks: BackgroundTasks | None = None):
        try:
            data = office_data.model_dump(exclude_none=True)
            if not data.get("external_id") or not data.get("name"):
                raise HTTPException(
                    status_code=400,
                    detail="external_id and name are required",
                )
            new_office = Office(**data)

            db.add(new_office)
            db.commit()
            db.refresh(new_office)

            if current_user and background_tasks:
                telegram_msg = (
                    f"<b>🎓 New Office Created:</b> {new_office.name}\n"
                    f"<b>👤 Created by:</b> {current_user.username}\n"
                    "==============================\n"
                )
                NotificationService.notify_action(
                    db=db,
                    user=current_user,
                    title="New Office Created",
                    message=f"Office {new_office.name} has been added",
                    link=f"/offices/views/{new_office.id}",
                    notification_type="office",
                    background_tasks=background_tasks,
                    telegram_message=telegram_msg,
                )

            return new_office

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def findAll(db):
        try:
            offices = (
                db.query(
                    Office.id,
                    Office.external_id,
                    Office.name,
                    Office.is_active,
                    Office.created_at,
                    Office.updated_at,
                    Office.is_delete,
                )
                .filter(Office.is_delete == False)
                .all()
            )

            return [dict(row._mapping) for row in offices]

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def findById(office_id, db):
        try:
            office = (
                db.query(
                    Office.id,
                    Office.external_id,
                    Office.name,
                    Office.is_active,
                    Office.created_at,
                    Office.updated_at,
                    Office.is_delete,
                )
                .filter(
                    Office.id == office_id,
                    Office.is_delete == False,
                )
                .first()
            )

            if not office:
                raise HTTPException(status_code=404, detail="Office not found")

            return dict(office._mapping)

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    @staticmethod
    def update(office_id, office_data, db, current_user, background_tasks):
        try:
            office = db.query(Office).filter(Office.id == office_id, Office.is_delete == False).first()

            if not office:
                raise HTTPException(status_code=404, detail="Office not found")

            update_data = office_data.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(office, key, value)

            db.commit()
            db.refresh(office)

            if current_user and background_tasks:
                telegram_msg = (
                    f"<b>🎓 Office Updated:</b> {office.name}\n"
                    f"<b>👤 Updated by:</b> {current_user.username}\n"
                    "==============================\n"
                )
                NotificationService.notify_action(
                    db=db,
                    user=current_user,
                    title="Office Updated",
                    message=f"Office {office.name} has been updated",
                    link=f"/offices/views/{office.id}",
                    notification_type="office",
                    background_tasks=background_tasks,
                    telegram_message=telegram_msg,
                )

            return office

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
    @staticmethod
    def deleted(office_id, db, current_user, background_tasks):
        try:
            office = db.query(Office).filter(Office.id == office_id).first()

            if not office:
                raise HTTPException(status_code=404, detail="Office not found")

            office.is_delete = True
            db.commit()

            if current_user and background_tasks:
                telegram_msg = (
                    f"<b>🎓 Office Deleted:</b> {office.name}\n"
                    f"<b>👤 Deleted by:</b> {current_user.username}\n"
                    "==============================\n"
                )
                NotificationService.notify_action(
                    db=db,
                    user=current_user,
                    title="Office Deleted",
                    message=f"Office {office.name} has been deleted",
                    link=f"/offices/views/{office.id}",
                    notification_type="office",
                    background_tasks=background_tasks,
                    telegram_message=telegram_msg,
                )

            return office

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
