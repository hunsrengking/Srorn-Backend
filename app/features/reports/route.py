from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.features.reports.controller import ReportController

router = APIRouter(prefix="/api")


@router.get("/reports-testing")
def get_reports_testing(db: Session = Depends(get_db)):
    return ReportController.get_reports_testing(db)


@router.get("/reports")
def get_reports(
    from_date: str | None = Query(None),
    to_date: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
):
    return ReportController.get_reports(db, from_date, to_date, status)


@router.get("/reports/export")
def export_reports(
    from_date: str | None = Query(None),
    to_date: str | None = Query(None),
    status: str | None = Query(None),
    export_type: Literal["csv", "excel", "pdf"] = Query("csv", alias="type"),
    db: Session = Depends(get_db),
):
    return ReportController.export_reports(
        db,
        from_date,
        to_date,
        status,
        export_type,
    )
