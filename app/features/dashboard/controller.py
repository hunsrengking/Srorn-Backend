from sqlalchemy.orm import Session

from app.features.dashboard.service import DashboardService


class DashboardController:
    @staticmethod
    def summary(db: Session):
        return DashboardService.get_summary(db)

    @staticmethod
    def tickets_by_date(db: Session):
        return DashboardService.tickets_by_date(db)

    @staticmethod
    def tickets_by_month(db: Session):
        return DashboardService.tickets_by_month(db)
