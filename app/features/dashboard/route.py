from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.dashboard.controller import DashboardController
from app.middlewares.auth_middlewares import require_permission

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    user=Depends(require_permission("VIEW_DASHBOARD")),
):
    return DashboardController.summary(db)


@router.get("/ticketsbydate")
def tickets_by_date(
    db: Session = Depends(get_db),
    user=Depends(require_permission("VIEW_DASHBOARD")),
):
    return DashboardController.tickets_by_date(db)


@router.get("/ticketsbymonth")
def tickets_by_month(
    db: Session = Depends(get_db),
    user=Depends(require_permission("VIEW_DASHBOARD")),
):
    return DashboardController.tickets_by_month(db)
