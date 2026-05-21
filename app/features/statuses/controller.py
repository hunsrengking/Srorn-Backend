from sqlalchemy.orm import Session

from app.features.statuses import service as status_service


class StatusController:
    @staticmethod
    def get_all_status(db: Session):
        return status_service.getAllStatus(db)

    @staticmethod
    def get_all_category(db: Session):
        return status_service.getAllCategory(db)

    @staticmethod
    def get_all_priority(db: Session):
        return status_service.getAllPriority(db)
