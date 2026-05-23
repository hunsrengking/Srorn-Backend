from decimal import Decimal

from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.features.notifications.service import NotificationService
from app.features.organization.positions.models import PositionRequest
from app.features.organization.positions.schema import Position


class PositionService:
    @staticmethod
    def getAllPosition(db: Session):
        return db.query(Position).order_by(Position.title).all()

    @staticmethod
    def _validate_salary(min_salary: Decimal | None, max_salary: Decimal | None):
        if min_salary is not None and min_salary < 0:
            raise HTTPException(status_code=400, detail="Min salary cannot be negative")

        if max_salary is not None and max_salary < 0:
            raise HTTPException(status_code=400, detail="Max salary cannot be negative")

        if min_salary is not None and max_salary is not None and min_salary > max_salary:
            raise HTTPException(
                status_code=400,
                detail="Min salary cannot be greater than Max salary",
            )

    @staticmethod
    def create_position(
        data: PositionRequest,
        db: Session,
        current_user=None,
        background_tasks: BackgroundTasks | None = None,
    ):
        try:
            if not data.title:
                raise HTTPException(status_code=400, detail="Position title is required")

            PositionService._validate_salary(data.min_salary, data.max_salary)

            position = Position(**data.model_dump(exclude_unset=True))
            db.add(position)
            db.commit()
            db.refresh(position)

            if current_user and background_tasks:
                telegram_msg = (
                    f"<b>New Position Created:</b> {position.title}\n"
                    f"<b>Created by:</b> {current_user.username}\n"
                    "==============================\n"
                )
                NotificationService.notify_action(
                    db=db,
                    user=current_user,
                    title="New Position Created",
                    message=f"Position {position.title} has been added",
                    link="/positions",
                    notification_type="position",
                    background_tasks=background_tasks,
                    telegram_message=telegram_msg,
                )

            return position

        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Position title already exists")

    @staticmethod
    def update_position(position_id: int, data: PositionRequest, db: Session):
        position = db.query(Position).filter(Position.id == position_id).first()

        if not position:
            raise HTTPException(status_code=404, detail="Position not found")

        try:
            PositionService._validate_salary(data.min_salary, data.max_salary)

            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(position, key, value)

            db.commit()
            db.refresh(position)
            return position

        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Update failed due to invalid data")

    @staticmethod
    def delete_position(position_id: int, db: Session):
        position = db.query(Position).filter(Position.id == position_id).first()

        if not position:
            raise HTTPException(status_code=404, detail="Position not found")

        try:
            db.delete(position)
            db.commit()
            return {"message": "Position deleted successfully"}

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Cannot delete position because it is in use",
            )
