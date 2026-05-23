from sqlalchemy.orm import Session

from app.features.organization.positions.service import PositionService
from app.features.organization.positions.models import PositionRequest


class PositionController:
    @staticmethod
    def get_all(db: Session):
        return PositionService.getAllPosition(db)

    @staticmethod
    def create(data: PositionRequest, db: Session, current_user, background_tasks):
        return PositionService.create_position(data, db, current_user, background_tasks)

    @staticmethod
    def update(position_id: int, data: PositionRequest, db: Session):
        return PositionService.update_position(position_id, data, db)

    @staticmethod
    def delete(position_id: int, db: Session):
        return PositionService.delete_position(position_id, db)
