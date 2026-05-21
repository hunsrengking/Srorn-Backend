from sqlalchemy.orm import Session

from app.features.dashboard import service as dashboard_service


class DashboardController:
    @staticmethod
    def summary(db: Session):
        return dashboard_service.get_summary(db)

    @staticmethod
    def tickets_by_date(db: Session):
        return dashboard_service.tickets_by_date(db)

    @staticmethod
    def tickets_by_month(db: Session):
        return dashboard_service.tickets_by_month(db)
