from sqlalchemy.orm import Session

from app.features.statuses.service import StatusService


class StatusController:
    @staticmethod
    def get_all_status(db: Session):
        return StatusService.getAllStatus(db)

    @staticmethod
    def get_all_category(db: Session):
        return StatusService.getAllCategory(db)

    @staticmethod
    def get_all_priority(db: Session):
        return StatusService.getAllPriority(db)
