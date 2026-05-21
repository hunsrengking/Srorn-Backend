from sqlalchemy.orm import Session

from app.features.positions import service as positions_service
from app.features.positions.models import PositionCreate, PositionUpdate


class PositionController:
    @staticmethod
    def get_all(db: Session):
        return positions_service.getAllPosition(db)

    @staticmethod
    def create(data: PositionCreate, db: Session, current_user, background_tasks):
        return positions_service.create_position(data, db, current_user, background_tasks)

    @staticmethod
    def update(position_id: int, data: PositionUpdate, db: Session):
        return positions_service.update_position(position_id, data, db)

    @staticmethod
    def delete(position_id: int, db: Session):
        return positions_service.delete_position(position_id, db)
