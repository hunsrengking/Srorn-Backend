from sqlalchemy import text
from sqlalchemy.orm import Session


class ReportService:
    @staticmethod
    def getReports(
        db: Session,
        from_date: str | None = None,
        to_date: str | None = None,
        status: str | None = None,
    ):
        from_date = None if from_date in (None, "", " ") else from_date.strip()
        to_date = None if to_date in (None, "", " ") else to_date.strip()
        status = None if status in (None, "", " ") else status.strip()

        sql = text(
            """
            SELECT *
            FROM v_ticket_reports
            WHERE
                (:from_date IS NULL OR create_date >= :from_date)
            AND (:to_date IS NULL OR create_date <= :to_date)
            AND (:status IS NULL OR status = :status)
            ORDER BY create_date DESC
            """
        )

        result = (
            db.execute(
                sql,
                {
                    "from_date": from_date,
                    "to_date": to_date,
                    "status": status,
                },
            )
            .mappings()
            .all()
        )

        return result
